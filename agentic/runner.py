"""Model-neutral agentic runner. A ReAct-style loop with a FIXED text tool protocol identical for
every model (no reliance on any vendor's native tool-calling). Sandboxed to a per-run working copy
of the task repo. Records the full transcript + metrics. Produces the model's final repo state for
the (separate, deterministic) verifier — the runner NEVER scores.

Usage: python runner.py <task_dir> <model_json> <out_dir>
  model_json: {"id","label","ep","key","shape":"openai"|"anthropic","pin","pout"}
Budgets (max_turns, max_tokens_per_turn) come from the task meta — IDENTICAL for all models.
"""
import json, os, sys, re, shutil, subprocess, time, urllib.request

TOOLS_DOC = """You are a software engineer working in a repository. Take ONE action per message.
Emit a single line beginning with `ACTION:`. Exactly these tools:
- ACTION: list_files
- ACTION: read_file <path>
- ACTION: run_command <shell command>        (runs in the repo root, 60s cap)
- ACTION: write_file <path>                  (then, on the following lines, put the COMPLETE new
                                              file content inside ONE fenced ``` code block)
- ACTION: finish                             (you are done; submit your changes)

Example of writing a file:
ACTION: write_file pkg/util.py
```python
def add(a, b):
    return a + b
```

Rules: make real edits with write_file (always give the FULL file, not a diff). You may run the
project's own tests to check yourself, but the final grade uses hidden tests you cannot see.
When the task is complete, emit `ACTION: finish`."""


def _post_openai(m, messages, max_tokens, timeout=180):
    body = json.dumps({"model": m["id"], "messages": messages, "temperature": 0.0,
                       "max_tokens": max_tokens, "stream": True,
                       "stream_options": {"include_usage": True}}).encode()
    req = urllib.request.Request(m["ep"], data=body, method="POST",
                                 headers={"Authorization": "Bearer " + m["key"], "Content-Type": "application/json"})
    t0 = time.time(); ttft = None; parts = []; ptok = ctok = 0
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        for raw in resp:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data:"):
                continue
            d = line[5:].strip()
            if d == "[DONE]":
                break
            try:
                o = json.loads(d)
            except Exception:
                continue
            for ch in o.get("choices") or []:
                delta = (ch.get("delta") or {}).get("content")
                if delta:
                    if ttft is None:
                        ttft = time.time() - t0
                    parts.append(delta)
            if o.get("usage"):
                ptok = o["usage"].get("prompt_tokens", 0) or 0
                ctok = o["usage"].get("completion_tokens", 0) or 0
    return {"text": "".join(parts), "ttft": ttft or (time.time() - t0), "in": ptok, "out": ctok}


def _post_anthropic(m, messages, max_tokens, timeout=240):
    # translate [{'role','content'}] -> anthropic; system message separated
    sys_txt = "\n".join(x["content"] for x in messages if x["role"] == "system")
    conv = [{"role": ("assistant" if x["role"] == "assistant" else "user"), "content": x["content"]}
            for x in messages if x["role"] != "system"]
    body = json.dumps({"model": m["id"], "max_tokens": max_tokens, "temperature": 0.0,
                       "system": sys_txt, "messages": conv}).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body, method="POST",
                                 headers={"x-api-key": m["key"], "anthropic-version": "2023-06-01",
                                          "content-type": "application/json"})
    t0 = time.time()
    o = json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode())
    txt = "".join(b.get("text", "") for b in o.get("content", []) if b.get("type") == "text")
    u = o.get("usage", {})
    return {"text": txt, "ttft": time.time() - t0, "in": u.get("input_tokens", 0), "out": u.get("output_tokens", 0)}


def call_model(m, messages, max_tokens):
    return _post_anthropic(m, messages, max_tokens) if m.get("shape") == "anthropic" else _post_openai(m, messages, max_tokens)


def parse_action(text):
    matches = list(re.finditer(r"(?m)^\s*ACTION:\s*(list_files|read_file|run_command|write_file|finish)\b[ \t]*(.*)$", text))
    if not matches:
        return None
    mm = matches[0]   # execute exactly ONE action per turn: the first the model emits
    tool, arg = mm.group(1), mm.group(2).strip()
    content = None
    if tool == "write_file":
        fence = re.search(r"```[^\n]*\n(.*?)```", text[mm.end():], re.S)
        content = fence.group(1) if fence else ""
    return {"tool": tool, "arg": arg, "content": content}


def safe_path(root, p):
    full = os.path.normpath(os.path.join(root, p))
    if not full.startswith(os.path.normpath(root)):
        raise ValueError("path escapes repo")
    return full


def exec_tool(root, action):
    t = action.get("tool"); arg = action.get("arg", ""); content = action.get("content")
    try:
        if t == "list_files":
            out = []
            for dp, _dn, fn in os.walk(root):
                for f in fn:
                    out.append(os.path.relpath(os.path.join(dp, f), root).replace("\\", "/"))
            return "FILES:\n" + "\n".join(sorted(out)[:400])
        if t == "read_file":
            return open(safe_path(root, arg), encoding="utf-8", errors="replace").read()[:12000]
        if t == "write_file":
            fp = safe_path(root, arg)
            os.makedirs(os.path.dirname(fp), exist_ok=True)
            open(fp, "w", encoding="utf-8").write(content or "")
            return "WROTE %s (%d bytes)" % (arg, len(content or ""))
        if t == "run_command":
            r = subprocess.run(arg, shell=True, cwd=root, capture_output=True, text=True, timeout=60)
            return ("exit=%d\nSTDOUT:\n%s\nSTDERR:\n%s" % (r.returncode, r.stdout[-4000:], r.stderr[-2000:]))
        return "unknown tool"
    except Exception as e:
        return "TOOL_ERROR: " + str(e)[:400]


def run(task_dir, model, out_dir):
    meta = json.load(open(os.path.join(task_dir, "meta.json")))
    prompt = open(os.path.join(task_dir, "prompt.md"), encoding="utf-8").read()
    work = os.path.join(out_dir, "repo")
    if os.path.exists(work):
        shutil.rmtree(work)
    shutil.copytree(os.path.join(task_dir, "repo"), work)

    max_turns = meta["max_turns"]; max_tok = meta["max_tokens_per_turn"]
    messages = [{"role": "system", "content": TOOLS_DOC},
                {"role": "user", "content": "TASK:\n" + prompt + "\n\nBegin. Take one action per message."}]
    transcript = []
    in_tok = out_tok = 0; ttft0 = None; t0 = time.time(); turns = 0; tool_counts = {}
    for turn in range(max_turns):
        turns += 1
        try:
            r = call_model(model, messages, max_tok)
        except Exception as e:
            transcript.append({"turn": turn, "error": str(e)[:300]})
            break
        if ttft0 is None:
            ttft0 = r["ttft"]
        in_tok += r["in"]; out_tok += r["out"]
        messages.append({"role": "assistant", "content": r["text"]})
        action = parse_action(r["text"])
        transcript.append({"turn": turn, "assistant": r["text"][:6000], "action": action,
                           "in": r["in"], "out": r["out"]})
        if not action or action.get("tool") == "finish":
            break
        tool_counts[action["tool"]] = tool_counts.get(action["tool"], 0) + 1
        obs = exec_tool(work, action)
        messages.append({"role": "user", "content": "OBSERVATION:\n" + obs[:8000]})
        transcript.append({"turn": turn, "observation": obs[:4000]})
    wall = time.time() - t0
    metrics = {"model": model["label"], "task": meta["id"], "category": meta["category"],
               "turns": turns, "input_tokens": in_tok, "output_tokens": out_tok,
               "ttft_s": round(ttft0 or 0, 3), "wall_s": round(wall, 1),
               "tool_calls": tool_counts,
               "api_cost_usd": round(in_tok / 1e6 * model.get("pin", 0) + out_tok / 1e6 * model.get("pout", 0), 4)}
    json.dump(metrics, open(os.path.join(out_dir, "metrics.json"), "w"), indent=2)
    json.dump(transcript, open(os.path.join(out_dir, "transcript.json"), "w"), indent=2)
    return metrics


if __name__ == "__main__":
    task_dir, model_json, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(out_dir, exist_ok=True)
    m = json.loads(open(model_json).read()) if os.path.exists(model_json) else json.loads(model_json)
    print(json.dumps(run(task_dir, m, out_dir), indent=2))
