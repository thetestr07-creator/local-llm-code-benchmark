"""Controlled, instrumented code benchmark — ONE harness, identical prompts/scoring/retry for every
model (no per-model tuning). Streams responses to measure TTFT + generation speed, samples GPU
power/VRAM/util to derive energy + electricity cost, preserves every raw response.

Phase 1: HumanEval + MBPP. Model-agnostic: local models via the OpenAI-compatible gateway; cloud
contenders (claude-sonnet-4-6, gpt-oss-120b) slot into the same MODELS list with their endpoint/key.
This invocation runs the LOCAL models only (no spend).
"""
import json, gzip, urllib.request, subprocess, tempfile, os, sys, time, re, threading

GW = "http://LOCAL_GATEWAY:18400/v1/chat/completions"
GKEY = open("<KEYFILE>").read().strip()
ELEC_RATE = 0.13  # $/kWh (owner's rate)
OUTDIR = "/home/user/bench_instrumented"
MAX_TOKENS = 1024
RETRY_ON_ERROR = 1          # identical retry policy for every model: 1 retry on transport error only

# --- model registry (local now; cloud entries added in the cloud phase, same schema) ---
MODELS = [
    {"id": "qwen25", "label": "Qwen2.5-Coder-14B", "ep": GW, "key": GKEY, "prov": "local", "pin": 0.0, "pout": 0.0},
    {"id": "phi4",   "label": "Phi-4",             "ep": GW, "key": GKEY, "prov": "local", "pin": 0.0, "pout": 0.0},
    {"id": "smart",  "label": "Qwen3-30B-A3B",     "ep": GW, "key": GKEY, "prov": "local", "pin": 0.0, "pout": 0.0},
]

HE_URL = "https://raw.githubusercontent.com/openai/human-eval/master/data/HumanEval.jsonl.gz"
MBPP_URL = "https://raw.githubusercontent.com/google-research/google-research/master/mbpp/sanitized-mbpp.json"


class GpuSampler(threading.Thread):
    """Samples both P100s every 2s: summed VRAM, avg util, summed power. Used to derive energy."""
    def __init__(self):
        super().__init__(daemon=True)
        self.samples = []
        self._stop = False

    def run(self):
        while not self._stop:
            try:
                out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,utilization.gpu,power.draw",
                                      "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=5).stdout
                rows = [r.split(",") for r in out.strip().splitlines() if r.strip()]
                if rows:
                    mem = sum(float(r[0]) for r in rows)
                    util = sum(float(r[1]) for r in rows) / len(rows)
                    pw = sum(float(r[2]) for r in rows)
                    self.samples.append((time.time(), mem, util, pw))
            except Exception:
                pass
            time.sleep(2)

    def stop(self):
        self._stop = True

    def window(self, t0, t1):
        s = [x for x in self.samples if t0 <= x[0] <= t1]
        if len(s) < 2:
            return {}
        mem = [x[1] for x in s]
        util = [x[2] for x in s]
        wh = 0.0
        for i in range(1, len(s)):
            dt = s[i][0] - s[i - 1][0]
            wh += (s[i][3] + s[i - 1][3]) / 2.0 * dt / 3600.0
        kwh = wh / 1000.0
        return {"vram_mb_peak": round(max(mem)), "gpu_util_avg_pct": round(sum(util) / len(util), 1),
                "power_w_avg": round(sum(x[3] for x in s) / len(s), 1), "power_w_peak": round(max(x[3] for x in s), 1),
                "energy_kwh": round(kwh, 5), "electricity_cost_usd": round(kwh * ELEC_RATE, 5)}


def stream_generate(m, content, timeout=180):
    body = json.dumps({"model": m["id"], "messages": [{"role": "user", "content": content}],
                       "temperature": 0.0, "max_tokens": MAX_TOKENS,
                       "stream": True, "stream_options": {"include_usage": True}}).encode()
    req = urllib.request.Request(m["ep"], data=body, method="POST",
                                 headers={"Authorization": "Bearer " + m["key"], "Content-Type": "application/json"})
    t0 = time.time()
    ttft = None
    parts = []
    ptok = ctok = ntok = 0
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        for raw in resp:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data:"):
                continue
            payload = line[5:].strip()
            if payload == "[DONE]":
                break
            try:
                obj = json.loads(payload)
            except Exception:
                continue
            for ch in obj.get("choices") or []:
                delta = (ch.get("delta") or {}).get("content")
                if delta:
                    if ttft is None:
                        ttft = time.time() - t0
                    parts.append(delta)
                    ntok += 1
            if obj.get("usage"):
                ptok = obj["usage"].get("prompt_tokens", 0) or 0
                ctok = obj["usage"].get("completion_tokens", 0) or 0
    wall = time.time() - t0
    out_tok = ctok or ntok
    gen_time = max(1e-6, wall - (ttft or 0))
    return {"text": "".join(parts), "ttft_s": round(ttft or wall, 3), "wall_s": round(wall, 3),
            "prompt_tokens": ptok, "completion_tokens": out_tok,
            "gen_tps": round(out_tok / gen_time, 1),
            "prefill_tps": round(ptok / ttft, 1) if (ttft and ptok) else 0,
            "t0": t0, "t1": t0 + wall}


def generate_with_retry(m, content):
    retries = 0
    last = None
    for attempt in range(RETRY_ON_ERROR + 1):
        try:
            r = stream_generate(m, content)
            r["retries"] = retries
            return r
        except Exception as e:
            last = str(e)[:150]
            retries += 1
    return {"text": "", "error": last, "retries": retries - 1, "ttft_s": 0, "wall_s": 0,
            "prompt_tokens": 0, "completion_tokens": 0, "gen_tps": 0, "prefill_tps": 0,
            "t0": time.time(), "t1": time.time()}


def code_of(text):
    mm = re.search(r"```(?:python)?\s*(.*?)```", text, re.S)
    return (mm.group(1) if mm else text).strip()


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


def load_humaneval():
    p = "/home/user/HumanEval.jsonl.gz"
    if not os.path.exists(p):
        urllib.request.urlretrieve(HE_URL, p)
    out = []
    with gzip.open(p, "rt", encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if ln:
                d = json.loads(ln)
                out.append({"id": d["task_id"], "kind": "humaneval", "prompt": d["prompt"],
                            "entry": d["entry_point"], "test": d["test"]})
    return out


def load_mbpp():
    p = "/home/user/sanitized-mbpp.json"
    if not os.path.exists(p):
        urllib.request.urlretrieve(MBPP_URL, p)
    return [{"id": "mbpp/%s" % d["task_id"], "kind": "mbpp", "prompt": d["prompt"],
             "tests": d["test_list"], "setup": d.get("test_imports", [])} for d in json.load(open(p, encoding="utf-8"))]


def prompt_for(prob):
    if prob["kind"] == "humaneval":
        return ("Complete this Python function. Return ONLY the complete function definition in a single "
                "```python code block, no prose.\n\n" + prob["prompt"])
    return ("Write a Python function for this task. It MUST pass these tests:\n" + "\n".join(prob["tests"]) +
            "\n\nTask: " + prob["prompt"] + "\nReturn ONLY the function in a single ```python code block, no prose.")


def score(prob, text):
    code = code_of(text)
    if prob["kind"] == "humaneval":
        ep = prob["entry"]
        prog = code if ("def %s" % ep) in code else (prob["prompt"] + "\n" + code)
        prog += "\n\n" + prob["test"] + "\n\ncheck(%s)\n" % ep
    else:
        prog = "\n".join(prob["setup"]) + "\n" + code + "\n" + "\n".join(prob["tests"]) + "\n"
    return run_prog(prog)


def bench(m, sname, probs, sampler, rawlog):
    agg = {"passed": 0, "total": 0, "retries": 0, "in_tok": 0, "out_tok": 0,
           "ttft": [], "gen_tps": [], "prefill_tps": [], "errors": 0}
    t_start = time.time()
    for i, prob in enumerate(probs):
        r = generate_with_retry(m, prompt_for(prob))
        ok = False
        if r.get("text"):
            try:
                ok = score(prob, r["text"])
            except Exception:
                ok = False
        else:
            agg["errors"] += 1
        agg["passed"] += 1 if ok else 0
        agg["total"] += 1
        agg["retries"] += r.get("retries", 0)
        agg["in_tok"] += r["prompt_tokens"]
        agg["out_tok"] += r["completion_tokens"]
        if r["ttft_s"]:
            agg["ttft"].append(r["ttft_s"])
        if r["gen_tps"]:
            agg["gen_tps"].append(r["gen_tps"])
        if r["prefill_tps"]:
            agg["prefill_tps"].append(r["prefill_tps"])
        rawlog.write(json.dumps({"model": m["id"], "suite": sname, "task": prob["id"], "pass": ok,
                                 "ttft_s": r["ttft_s"], "gen_tps": r["gen_tps"], "in_tok": r["prompt_tokens"],
                                 "out_tok": r["completion_tokens"], "retries": r.get("retries", 0),
                                 "raw": r.get("text", "")[:4000]}) + "\n")
        rawlog.flush()
        if (i + 1) % 40 == 0:
            print("  [%s/%s] %d/%d pass@1=%.1f%%" % (m["label"], sname, i + 1, len(probs),
                  100.0 * agg["passed"] / agg["total"]), flush=True)
    t_end = time.time()
    gpu = sampler.window(t_start, t_end) if m["prov"] == "local" else {}
    n = agg["total"]
    def avg(x):
        return round(sum(x) / len(x), 2) if x else 0
    api_cost = round(agg["in_tok"] / 1e6 * m["pin"] + agg["out_tok"] / 1e6 * m["pout"], 4)
    return {"suite": sname, "model": m["label"], "provider": m["prov"],
            "pass_at_1": round(100.0 * agg["passed"] / n, 1), "passed": agg["passed"], "total": n,
            "task_success_rate": round(100.0 * agg["passed"] / n, 1), "gen_errors": agg["errors"],
            "retries_total": agg["retries"], "input_tokens": agg["in_tok"], "output_tokens": agg["out_tok"],
            "ttft_s_avg": avg(agg["ttft"]), "prefill_tps_avg": avg(agg["prefill_tps"]),
            "gen_tps_avg": avg(agg["gen_tps"]), "wall_clock_s": round(t_end - t_start),
            "api_cost_usd": api_cost, **gpu}


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    suites = {"HumanEval": load_humaneval(), "MBPP": load_mbpp()}
    print("loaded HumanEval=%d MBPP=%d" % (len(suites["HumanEval"]), len(suites["MBPP"])), flush=True)
    sampler = GpuSampler()
    sampler.start()
    results = []
    for m in MODELS:
        rawlog = open(os.path.join(OUTDIR, "raw_%s.jsonl" % m["id"]), "w")
        for sname, probs in suites.items():
            print("=== %s on %s ===" % (m["label"], sname), flush=True)
            try:
                results.append(bench(m, sname, probs, sampler, rawlog))
            except Exception as e:
                results.append({"suite": sname, "model": m["label"], "error": str(e)[:200]})
            json.dump(results, open(os.path.join(OUTDIR, "instrumented_results.json"), "w"), indent=2)
        rawlog.close()
    sampler.stop()
    subprocess.run(["python3", "/home/user/swap.py", "fast"], capture_output=True)
    open(os.path.join(OUTDIR, "PHASE1_DONE"), "w").write(str(int(time.time())))
    print("PHASE1_DONE", flush=True)


if __name__ == "__main__":
    main()
