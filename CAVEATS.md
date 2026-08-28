# CAVEATS — read this before judging the numbers

I'd rather state the weaknesses myself than have someone "expose" them. Here they are.

1. **HumanEval and MBPP are almost certainly in every model's training data** (local and cloud). The
   code-gen numbers are inflated for everyone and mostly measure recall, not generalization. That's
   exactly why I also built the agentic benchmark with novel, hand-made tasks and hidden tests — those
   are the numbers I actually trust.

2. **Small sample.** 18 agentic tasks (16 after exclusions) is a *directional* signal, not a
   statistically powered result. No confidence intervals. Add tasks and re-run — the harness is here.

3. **Two tasks were excluded after the freeze.** The frozen set was 18. Two turned out to have
   ambiguous specs that even Sonnet's reasonable solutions failed (`multiedit-03`: the hidden test
   demanded a module path the prompt never specified; `testexec-02`: it rejected the locale-ambiguous
   input `'1,23'`). Both tasks and their verify logs are included. I report BOTH the raw 18-task and the
   16-clean numbers. Note removing them *raised* the local models' percentages — it did not flatter cloud.

4. **"Frozen" is a SHA-256 manifest computed before the cloud run** (timestamps in the logs), but it is
   not third-party notarized — a stranger cannot prove I didn't backdate it. The defense is that every
   task and test is published, so the results stand on their own regardless.

5. **pass@1, greedy, temperature 0** — a single deterministic sample per problem. No pass@k, no variance.

6. **The $0.04 is GPU-card energy only** (nvidia-smi `power.draw` × time × $0.13/kWh). It excludes CPU,
   PSU inefficiency, cooling, idle draw, hardware amortization, and my time. It is the *marginal* cost of
   running the box I already own — not "local is free" and not total cost of ownership.

7. **Local models are Q4_K_M (4-bit quantized)** — weaker than their full weights. I benchmarked them as
   I actually run them; full precision would likely narrow the gap, not widen it.

8. **Task authoring was AI-assisted (Claude family), and Sonnet is Claude family.** Possible bias. The
   mitigation is that all tasks are published and are ordinary software tasks; if they were secretly
   Claude-biased, the local models wouldn't have cleared 10–13 of them.

9. **Transport differs between local (streaming gateway) and cloud (REST APIs).** Prompts, decoding
   params, tools, budgets, and scoring are identical and published; only the wire format differs, which
   is unavoidable across different APIs.

10. **llama.cpp with batching is not bit-exact deterministic** even at temp 0. Two local runs produced
    the same pass@1 (87.8/85.0), and all raw outputs are saved, but I don't claim bit-exact reproducibility.

**Sonnet 4.6 is the strongest model I can access in my setup — not a claim that it's the best model on earth.**
