# FORGE Live Evaluation v0.4

**Callout:** `FORGE Live Evaluate:` (may also invoke `FORGE Evaluate:` for offline runs).
This module evaluates **captured actual external outputs**. Its first implementation is manual import, not a live model provider. If API provider execution is unavailable, do not call the import a live invocation.

## 6-phase workflow
1. **Benchmark contract:** Use `benchmarks/live-suite.json` (all five categories) or validated custom suite. Fix tasks, source snapshots, acceptance criteria and baseline comparison rules before generating candidates.
2. **Capture:** Produce baseline and FORGE variants under controlled conditions externally. Save UTF-8 outputs and provenance. Import with `engine/live.py capture`, one output/case per record. Capture output text and SHA-256. Do not fabricate model configuration, latency, cost, or timestamps.
3. **Evaluate:** Run `engine/live.py evaluate` on imported run JSON. Deterministic checks pass/fail; semantic/manual checks remain `needs-human-review`.
4. **Compare:** Run `engine/live.py compare`. Exact task identity is enforced. Matching model string alone does not establish experimental equivalence. Report improvements, regressions and pending reviews.
5. **Automate:** GitHub Actions workflow manually runs structural tests and fixture evaluations. No secrets or external model calls. Uploaded result files must not contain sensitive data.
6. **Integrate:** Use v0.4 callout in ChatGPT project instructions; carry result with linked source and evidence into a review-gated improvement proposal.

## Demonstration
```bash
python engine/live.py capture --out /tmp/forge-run.json --task-id pilot --run-id candidate-1 --arm forge --source-ref local-file --output response.txt --case-id math-01 --model unknown
python engine/live.py evaluate --suite benchmarks/live-suite.json --run /tmp/forge-run.json
```
The partial example reports missing-category failures because the suite requires all five tasks. This is intentional.

## Release controls
No auto-approval, self-rewriting modules, auto-merge or claims of independent human review. Manual evaluation check results require human-supplied signed review outside this utility. Current text-based checker cannot validate binary slide/document rendering. Future provider adapters require explicit supported credentials, permission scoping, provider contracts, and spend safeguards.
