"""Full local-model code benchmark suite: HumanEval (164) + MBPP-sanitized (~427), pass@1.
Runs on a local GPU rig (isolated, localhost to the models). For each model x benchmark it prompts via the
gateway, EXECUTES the real unit tests in a sandboxed subprocess, and computes pass@1.
Writes suite_results.json + suite_report.md + a DONE marker. Restores the pinned fast pair at the end.
"""
import json, gzip, urllib.request, subprocess, tempfile, os, sys, time, re

GW = "http://LOCAL_GATEWAY:18400/v1/chat/completions"
GKEY = open("<KEYFILE>").read().strip()
HE_URL = "https://raw.githubusercontent.com/openai/human-eval/master/data/HumanEval.jsonl.gz"
MBPP_URL = "https://raw.githubusercontent.com/google-research/google-research/master/mbpp/sanitized-mbpp.json"
HE = "/home/user/HumanEval.jsonl.gz"
MBPP = "/home/user/sanitized-mbpp.json"
OUT = "/home/user/suite_results.json"
MD = "/home/user/suite_report.md"
DONE = "/home/user/suite_DONE"

MODELS = [("qwen25", "Qwen2.5-Coder-14B (coder)"),
          ("phi4",   "Phi-4 (reviewer)"),
          ("smart",  "Qwen3-30B-A3B (30B)")]


def load_humaneval():
    if not os.path.exists(HE):
        urllib.request.urlretrieve(HE_URL, HE)
    out = []
    with gzip.open(HE, "rt", encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if ln:
                p = json.loads(ln)
                out.append({"id": p["task_id"], "prompt": p["prompt"], "entry": p["entry_point"],
                            "test": p["test"], "kind": "humaneval"})
    return out


def load_mbpp():
    if not os.path.exists(MBPP):
        urllib.request.urlretrieve(MBPP_URL, MBPP)
    data = json.load(open(MBPP, encoding="utf-8"))
    out = []
    for p in data:
        out.append({"id": "mbpp/%s" % p["task_id"],
                    "prompt": p["prompt"], "tests": p["test_list"],
                    "setup": p.get("test_imports", []), "kind": "mbpp"})
    return out


def gen(model, content, timeout=150):
    body = json.dumps({"model": model, "temperature": 0.0, "max_tokens": 1024,
                       "messages": [{"role": "user", "content": content}]}).encode()
    req = urllib.request.Request(GW, data=body, method="POST",
                                 headers={"Authorization": "Bearer " + GKEY, "Content-Type": "application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode())
    return r["choices"][0]["message"]["content"], (r.get("usage") or {})


def code_of(text):
    m = re.search(r"```(?:python)?\s*(.*?)```", text, re.S)
    return (m.group(1) if m else text).strip()


def run_prog(prog, timeout=12):
    fd, path = tempfile.mkstemp(suffix=".py")
    os.close(fd)
    open(path, "w").write(prog)
    try:
        return subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=timeout).returncode == 0
    except Exception:
        return False
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


def check_humaneval(prob, completion):
    code = code_of(completion)
    ep = prob["entry"]
    prog = code if ("def %s" % ep) in code else (prob["prompt"] + "\n" + code)
    prog += "\n\n" + prob["test"] + "\n\ncheck(%s)\n" % ep
    return run_prog(prog)


def check_mbpp(prob, completion):
    code = code_of(completion)
    prog = "\n".join(prob["setup"]) + "\n" + code + "\n" + "\n".join(prob["tests"]) + "\n"
    return run_prog(prog)


def prompt_for(prob):
    if prob["kind"] == "humaneval":
        return ("Complete this Python function. Return ONLY the complete function definition in a "
                "single ```python code block, no prose.\n\n" + prob["prompt"])
    return ("Write a Python function for this task. It MUST pass these tests:\n" +
            "\n".join(prob["tests"]) + "\n\nTask: " + prob["prompt"] +
            "\nReturn ONLY the function in a single ```python code block, no prose.")


def bench(model, label, probs):
    passed = total = ptoks = ctoks = errs = 0
    t0 = time.time()
    for i, prob in enumerate(probs):
        ok = False
        try:
            comp, usage = gen(model, prompt_for(prob))
            ptoks += usage.get("prompt_tokens", 0) or 0
            ctoks += usage.get("completion_tokens", 0) or 0
            ok = check_humaneval(prob, comp) if prob["kind"] == "humaneval" else check_mbpp(prob, comp)
        except Exception:
            errs += 1
        passed += 1 if ok else 0
        total += 1
        if (i + 1) % 40 == 0:
            print("  [%s] %d/%d pass@1=%.1f%%" % (label, i + 1, len(probs), 100.0 * passed / total), flush=True)
    return {"pass_at_1": round(100.0 * passed / total, 1), "passed": passed, "total": total,
            "gen_errors": errs, "prompt_tokens": ptoks, "completion_tokens": ctoks, "secs": round(time.time() - t0)}


def main():
    for f in (OUT, MD, DONE):
        if os.path.exists(f):
            os.remove(f)
    suites = {"HumanEval": load_humaneval(), "MBPP": load_mbpp()}
    print("loaded HumanEval=%d MBPP=%d" % (len(suites["HumanEval"]), len(suites["MBPP"])), flush=True)
    results = {}
    for model, label in MODELS:
        results[label] = {}
        for sname, probs in suites.items():
            print("=== %s on %s ===" % (label, sname), flush=True)
            try:
                results[label][sname] = bench(model, label, probs)
            except Exception as e:
                results[label][sname] = {"error": str(e)[:200]}
            json.dump(results, open(OUT, "w"), indent=2)
    subprocess.run(["python3", "/home/user/swap.py", "fast"], capture_output=True)  # restore pinned pair

    lines = ["# localstack local models — code benchmarks (pass@1)", "",
             "_HumanEval (164) + MBPP-sanitized (427). Greedy decode, real unit-test execution, $0 (local GPUs)._", "",
             "| model | HumanEval | MBPP |", "|---|---|---|"]
    for _m, label in MODELS:
        r = results.get(label, {})
        he = r.get("HumanEval", {})
        mb = r.get("MBPP", {})
        lines.append("| %s | %s | %s |" % (
            label,
            ("%.1f%%" % he["pass_at_1"]) if "pass_at_1" in he else "err",
            ("%.1f%%" % mb["pass_at_1"]) if "pass_at_1" in mb else "err"))
    open(MD, "w").write("\n".join(lines) + "\n")
    open(DONE, "w").write(str(int(time.time())))
    print("SUITE_DONE", flush=True)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
