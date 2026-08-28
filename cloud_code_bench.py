"""Part 2 (code): run the CLOUD contenders through the identical HumanEval+MBPP harness the local
models used (same prompts, same scoring, executed on a local GPU rig). Sonnet 4.6 (Anthropic) + gpt-oss-120b
(DigitalOcean). Records pass@1, tokens, wall, and API $. Reuses benchmark_suite's scoring verbatim."""
import json, time, urllib.request, sys
sys.path.insert(0, "/home/user")
import benchmark_suite as B   # same loaders + scoring as the local run

KEYS = json.load(open("/home/user/_bench_keys.json"))
OUT = "/home/user/cloud_code_results.json"
MODELS = [
    {"id": "claude-sonnet-4-6", "label": "Claude Sonnet 4.6", "shape": "anthropic",
     "key": KEYS["anthropic"], "pin": 3.0, "pout": 15.0},
    {"id": "openai-gpt-oss-120b", "label": "GPT-oss-120b (DO)", "shape": "openai",
     "ep": "https://inference.do-ai.run/v1/chat/completions", "key": KEYS["do"], "pin": 0.1, "pout": 0.7},
]


def gen(m, content, timeout=150):
    if m["shape"] == "anthropic":
        body = json.dumps({"model": m["id"], "max_tokens": 1024, "temperature": 0.0,
                           "messages": [{"role": "user", "content": content}]}).encode()
        req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body,
                                     headers={"x-api-key": m["key"], "anthropic-version": "2023-06-01",
                                              "content-type": "application/json"})
        o = json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode())
        txt = "".join(b.get("text", "") for b in o.get("content", []) if b.get("type") == "text")
        u = o.get("usage", {})
        return txt, u.get("input_tokens", 0) or 0, u.get("output_tokens", 0) or 0
    body = json.dumps({"model": m["id"], "max_tokens": 1024, "temperature": 0.0,
                       "messages": [{"role": "user", "content": content}]}).encode()
    req = urllib.request.Request(m["ep"], data=body, method="POST",
                                 headers={"Authorization": "Bearer " + m["key"], "Content-Type": "application/json"})
    o = json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode())
    txt = o["choices"][0]["message"]["content"]
    u = o.get("usage", {})
    return txt, u.get("prompt_tokens", 0) or 0, u.get("completion_tokens", 0) or 0


def bench(m, sname, probs):
    passed = total = intok = outtok = errs = 0
    t0 = time.time()
    for i, prob in enumerate(probs):
        ok = False
        try:
            txt, it, ot = gen(m, B.prompt_for(prob))
            intok += it
            outtok += ot
            ok = B.check_humaneval(prob, txt) if prob["kind"] == "humaneval" else B.check_mbpp(prob, txt)
        except Exception:
            errs += 1
        passed += 1 if ok else 0
        total += 1
        if (i + 1) % 40 == 0:
            print("  [%s/%s] %d/%d pass@1=%.1f%% $%.2f" % (m["label"], sname, i + 1, len(probs),
                  100.0 * passed / total, intok / 1e6 * m["pin"] + outtok / 1e6 * m["pout"]), flush=True)
    cost = round(intok / 1e6 * m["pin"] + outtok / 1e6 * m["pout"], 4)
    return {"model": m["label"], "suite": sname, "pass_at_1": round(100.0 * passed / total, 1),
            "passed": passed, "total": total, "gen_errors": errs, "input_tokens": intok,
            "output_tokens": outtok, "api_cost_usd": cost, "wall_s": round(time.time() - t0)}


def main():
    suites = {"HumanEval": B.load_humaneval(), "MBPP": B.load_mbpp()}
    print("loaded HE=%d MBPP=%d" % (len(suites["HumanEval"]), len(suites["MBPP"])), flush=True)
    results = []
    spent = 0.0
    for m in MODELS:
        for sname, probs in suites.items():
            print("=== %s on %s ===" % (m["label"], sname), flush=True)
            try:
                r = bench(m, sname, probs)
                spent += r["api_cost_usd"]
                results.append(r)
            except Exception as e:
                results.append({"model": m["label"], "suite": sname, "error": str(e)[:200]})
            json.dump({"results": results, "spent_usd": round(spent, 3)}, open(OUT, "w"), indent=2)
            print("   running spend: $%.2f" % spent, flush=True)
    open("/home/user/CLOUD_CODE_DONE", "w").write(str(round(spent, 3)))
    print("CLOUD_CODE_DONE spent=$%.2f" % spent, flush=True)


main()
