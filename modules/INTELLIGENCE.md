# FORGE Intelligence + Evaluation v0.3.0

This is a **working deterministic evaluation and capability-selection scaffold**, not autonomous AI or multi-provider model execution.

## Calls
- `FORGE Evaluate:` run a benchmark against provided candidate outputs and, optionally, a baseline.
- `FORGE Select:` identify eligible providers from declared capabilities; verify any pricing, access, permissions and model availability externally before actual execution.
- `FORGE Improve:` compare baseline and candidate, flag regressions, propose repairs. Only implement with explicit authority.

## Evaluation contract
The suite declares fixed assertion types; the result fixture contains independently obtained outputs. Evaluation treats absent results as failures. Evidence must include a source and an observation. Gate requires all candidate cases passing and zero regressions. Do not confuse synthetic fixtures with independent model benchmark performance.

Commands:
`python engine/evaluate.py --suite benchmarks/suite.json --baseline benchmarks/fixtures/baseline.json --candidate benchmarks/fixtures/candidate.json --out reports/comparison.json`
`python -m unittest discover -s tests -v`

## Model/tool selection
`engine/selector.py` performs capability/budget filtering over `registry/providers.json`. Disabled or unavailable models are never selected. Unknown price fails budget checks; no platform model entitlements inferred. Selection is a plan, never an invoked tool call.

## Follow-on release criteria
Real-world, permissioned datasets and outputs; blind reviewer calibration; tracing for actual tool invocations; privacy-sensitive data handling; provider SDK adapters; per-task latency, quality and token/cost telemetry. No self-rewriting of approved modules or auto-merge based on synthetic tests.
