"""Deterministic verifier. Overlays the task's HELD-OUT tests onto a model's final repo state and
runs them in isolation. The model never sees these tests; this code alone decides pass/fail.
Same held-out suite + same solution -> same verdict, every time.

Usage: python verify.py <task_dir> <solution_repo_dir> <out_dir>
"""
import json, os, sys, shutil, subprocess, time


def verify(task_dir, solution_repo, out_dir):
    meta = json.load(open(os.path.join(task_dir, "meta.json")))
    evald = os.path.join(out_dir, "eval")
    if os.path.exists(evald):
        shutil.rmtree(evald)
    shutil.copytree(solution_repo, evald)
    # overlay held-out tests (authoritative; overwrite anything the model may have placed there)
    heldout = os.path.join(task_dir, "heldout")
    for dp, _dn, fn in os.walk(heldout):
        for f in fn:
            src = os.path.join(dp, f)
            rel = os.path.relpath(src, heldout)
            dst = os.path.join(evald, "__heldout__", rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy(src, dst)
    cmd = meta["heldout_cmd"]
    t0 = time.time()
    try:
        r = subprocess.run(cmd, shell=True, cwd=evald, capture_output=True, text=True, timeout=120)
        rc, out, err = r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        rc, out, err = 124, "", "TIMEOUT"
    passed = (rc == 0)
    log = "cmd: %s\nexit: %s\ndur_s: %.1f\nSTDOUT:\n%s\nSTDERR:\n%s" % (cmd, rc, time.time() - t0, out[-6000:], err[-3000:])
    open(os.path.join(out_dir, "verify_log.txt"), "w", encoding="utf-8").write(log)
    result = {"task": meta["id"], "category": meta["category"], "passed": passed, "exit_code": rc}
    json.dump(result, open(os.path.join(out_dir, "verify_result.json"), "w"), indent=2)
    return result


if __name__ == "__main__":
    print(json.dumps(verify(sys.argv[1], sys.argv[2], sys.argv[3]), indent=2))
