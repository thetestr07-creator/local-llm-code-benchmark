# 2026 Model Refresh

After the first release, a fair question came up: *"why benchmark 2-year-old models?"* So I ran a
batch of current (2026) open-weight models through the **exact same frozen harness** — same
HumanEval + MBPP problems, same scoring, same settings (`temperature 0`, `max_tokens 1024`, every
solution's code executed against the real unit tests). Nothing about the methodology changed; only
the models are new. All ran locally on the same 2× Tesla P100 (16 GB) rig.

## Results — pass@1 (code executed against real tests)

| Model | Type | HumanEval | MBPP | Full-suite wall-clock |
|---|---|---|---|---|
| **Qwen3-Coder-30B-A3B** | MoE (30B/3B active) | **92.1** | **85.2** | ~25 min |
| Gemma-3-27B | dense | 87.8 | 86.9 | ~154 min |
| Mistral-Small-3.2-24B | dense | 86.6 | — (incomplete) | — |
| Devstral-Small-2507-24B | dense | 86.0 | 77.0 | ~82 min |
| Qwen3-30B-A3B-Instruct-2507 | MoE (30B/3B active) | 81.7 | 85.0 | ~20 min |
| Qwen3-14B | dense | 87.8 | 82.0 | thinking disabled — see note |
| — *baselines from the original release* — | | | | |
| *Qwen2.5-Coder-14B (current stack)* | dense | 87.8 | 85.0 | — |
| *Phi-4 (current stack)* | dense | 86.0 | 82.4 | — |

## Takeaways
- **Qwen3-Coder-30B-A3B is the standout**: +4.3 HumanEval over the current Qwen2.5-Coder-14B (92.1 vs
  87.8), tied on MBPP, and because it's MoE (only ~3B params active per token) it ran the **whole suite
  ~3× faster than the dense 24B models**. Bigger model, better score, less wall-clock.
- **Gemma-3-27B** is a strong generalist (best MBPP of the challengers).
- **Devstral** underperforms on raw pass@1 — no surprise, it's tuned for *agentic* work, which HumanEval/
  MBPP don't measure. Its strength wouldn't show here.
- **Qwen3-14B (thinking off) is essentially level with the current Qwen2.5-Coder-14B** — 87.8 tied on
  HumanEval, a touch behind on MBPP (82.0 vs 85.0). At the single-GPU size the current pick still holds
  up; the real gain is stepping up to the Qwen3-Coder-30B MoE, which fits the same 2-card budget.

## Notes / honesty
- Every caveat in `CAVEATS.md` still applies — most importantly, HumanEval and MBPP are almost
  certainly in these models' training data too, so treat these as recall/parity numbers, not proof of
  generalization. They're here because the skeptic asked for a like-for-like comparison on the *same*
  harness, and that's exactly what this is.
- **Qwen3-14B was run with its "thinking" mode disabled** (`/no_think`, and any `<think>…</think>`
  block stripped before scoring). Left on, its chain-of-thought overran the 1024-token budget and
  buried the code, which isn't a fair code-gen measurement. All other models have no thinking mode, so
  this puts it on equal footing. Disclosed here rather than hidden.
- These runs are a model bake-off for *my own* stack decision. They were **not** part of the original
  frozen manifest, and I'm keeping them clearly separate from it — the frozen set and its raw outputs
  are unchanged.
