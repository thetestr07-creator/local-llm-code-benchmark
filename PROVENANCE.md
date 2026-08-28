# Provenance & How to Verify

## What this repository is
This is a **sanitized, self-contained export** of a local-LLM coding benchmark I ran on my
own hardware (2× NVIDIA Tesla P100, 16 GB each). It contains the harness, the tasks, the
**raw model outputs**, and the **scoring code** — everything needed to check the numbers
independently.

## Why there isn't a long commit history here
The benchmark was developed and executed inside a **private, isolated, self-hosted GitLab
environment** that also holds unrelated proprietary code. This GitHub repository is a
**clean, point-in-time export of just the benchmark** — not the working repo. So the commit
history here is short *by design*. I am not asking anyone to trust a commit log.

## Why you can trust the results anyway — don't trust me, re-run it
Every score in this repo is reproducible from the files provided:

- The **raw completions** from each model are saved verbatim (`raw_*.jsonl`).
- The **exact scoring code** that produced the pass@1 numbers is included.
- Re-running that scorer over the saved outputs reproduces the reported numbers **exactly**
  (e.g. Qwen2.5-Coder-14B → 87.8% HumanEval, an exact match). See `BENCHMARK_AUDIT.md`.
- The task set, runner, and scorer are pinned by **SHA-256 in
  `agentic/FROZEN_MANIFEST.json`**, so you can confirm nothing was swapped after the fact.

If you think a score is wrong, you don't have to take my word for it — score the raw outputs
yourself and compare.

## What is NOT in here (and why that's fine)
- **No proprietary or company code.** The coding tasks are the public **HumanEval** (OpenAI)
  and **MBPP** (Google) sets, plus small **synthetic toy repos** written specifically for the
  agentic tests. None of my product code is included, and none is required to reproduce
  anything.
- Internal hostnames, IP addresses, and file paths were masked during export (including
  inside serving-config metadata and the agent transcripts). This masking **did not alter any
  score, any pass/fail result, or the hash-locked task/runner/scorer set**: every file listed
  in `agentic/FROZEN_MANIFEST.json` is byte-identical to when it was frozen, and the raw model
  completions being scored (`results/raw_*.jsonl`) are unmodified.

## Going forward
Future benchmark rounds will be published on this GitHub account, and I intend to run them
**in the open** here so the run history is public from here on. This first release is the
existing evidence, exported clean from the private environment it was produced in.
