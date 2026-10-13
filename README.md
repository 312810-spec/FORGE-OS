# FORGE OS

**Reusable, versioned, evidence-led AI framework** · v0.3.0 candidate

FORGE OS is a methodology and lightweight execution-quality toolkit, not a general-purpose computer operating system. **AI prepares. User reviews. User approves.**

## Start
- [ChatGPT Project adapter v0.3](integrations/CHATGPT_V03.md) — scoped, manually configured callouts
- [Core](core/OPERATING_CONTRACT.md) and [module registry](registry/modules.json)
- [Intelligence and Evaluation](modules/INTELLIGENCE.md)
- [Research cross-reference](research/V0.2-CROSS-REFERENCE.md)
- [Release quality gates](quality/GATES.md)

## Runnable checks
```bash
python scripts/validate.py
python -m unittest discover -s tests -v
python engine/router.py --json "FORGE Assurance: audit draft"
python engine/evaluate.py --suite benchmarks/suite.json --baseline benchmarks/fixtures/baseline.json --candidate benchmarks/fixtures/candidate.json
```

## Scope and honesty
v0.3 implements deterministic capability-based routing and regression evaluation with synthetic fixtures. The candidate fixture is hand-authored, not produced by a live model; its improved score is not proof of better AI results. GitHub Actions tests and archives reports. No provider SDK, live model execution, actual per-token billing, independent human grading or autonomous module improvement is implemented. Other ChatGPT projects require the integration contract and accessible source.

See [v0.2 design](decisions/0002-v02.md) and [v0.3 decision](decisions/0003-v03.md).
