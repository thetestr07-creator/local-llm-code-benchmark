# Local vs Cloud Coding Benchmark — Evidence Package

A frozen benchmark of self-hosted local models vs Claude Sonnet 4.6 (and GPT-oss-120b) on
HumanEval + MBPP and 18 hand-built agentic repo tasks. Everything here is the raw artifact as it
was produced — nothing was re-run or cleaned up for release.

**Read `CAVEATS.md` first. The honest limitations are stated up front, on purpose.**

## Models
| Model | Where | Quant |
|---|---|---|
| Qwen2.5-Coder-14B | local (2× Tesla P100) | Q4_K_M GGUF |
| Phi-4 | local | Q4_K_M GGUF |
| Qwen3-30B-A3B | local | Q4_K_M GGUF |
| Claude Sonnet 4.6 | cloud (Anthropic API) | — |
| GPT-oss-120b | cloud (DigitalOcean) | — |

## Results
### Code — pass@1 (every solution's code executed against the real unit tests)
| Model | HumanEval | MBPP |
|---|---|---|
| Claude Sonnet 4.6 | 97.0 | 93.4 |
| GPT-oss-120b | 87.2 | 92.7 |
| Qwen2.5-Coder-14B | 87.8 | 85.0 |
| Phi-4 | 86.0 | 82.4 |
| Qwen3-30B-A3B | 81.7 | 85.0 |

Local code run = 1,773 problems, ~0.33 kWh GPU energy ≈ $0.04 @ $0.13/kWh. **GPU-card energy only — see CAVEATS.**

### Agentic — 18 hand-built repo tasks with hidden held-out tests
- **Raw (all 18):** Sonnet 16/18 · Phi-4 13/18 · Qwen3-30B 12/18 · Qwen2.5-14B 10/18
- 2 tasks (`multiedit-03-coupons`, `testexec-02-moneyfmt`) had ambiguous specs that **even Sonnet failed** — the full tasks and the failing verify logs are included (`results/agentic_cloud/`). Judge them yourself.
- **On the 16 clean tasks:** Sonnet 16/16 · Phi-4 13/16 · Qwen3-30B 12/16 · Qwen2.5-14B 10/16
- **GPT-oss agentic is excluded** — the harness could not capture its output format (transcripts are empty). It is NOT a claim that gpt-oss is weak; its code numbers above are included.

## What's here
- `benchmark_instrumented.py`, `benchmark_suite.py`, `cloud_code_bench.py` — code harness + scoring
- `agentic/runner.py`, `agentic/verify.py` — agentic harness. **The runner never copies the held-out tests into the model's workspace; the verifier overlays them only after the agent finishes.**
- `agentic/tasks/` — all 18 tasks: starting `repo/`, hidden `heldout/`, `meta.json`
- `agentic/FROZEN_MANIFEST.json` — SHA-256 of every task file + harness, computed before the cloud run
- `results/provenance.json` — model GGUF SHA-256s, quant, dataset SHA-256s, exact serving flags, inference settings
- `results/*.json` — every score
- `results/raw_*.jsonl` — every raw local code generation (all 1,773)
- `results/agentic_*/` — agentic scores, per-run transcripts, and verify logs

## Reproduce
Point the harness at your own model endpoints. Datasets are referenced by SHA-256 in `provenance.json`
(HumanEval = openai/human-eval; MBPP-sanitized = google-research/google-research) and not redistributed here.

## Not included / disclosure
No API keys, no credentials, and no private infrastructure code — the benchmark never contained any.
Internal hostnames, IP addresses, and file paths were removed/masked during export (see `PROVENANCE.md`).
That masking did **not** alter any score or the hash-locked task/runner/scorer set. The datasets
(HumanEval, MBPP) are referenced by SHA-256, not redistributed.
