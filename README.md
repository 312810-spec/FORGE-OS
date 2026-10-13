# FORGE OS

**Modular evidence-led AI framework** · v0.4 candidate

FORGE is not a traditional operating system. Its core commitment is **AI prepares; human reviews and approves**.

## v0.4: actual-output evaluation
- [Live Evaluation module](modules/LIVE_EVALUATION.md) and [ChatGPT adapter](integrations/CHATGPT_V04.md)
- [Five-category benchmark suite](benchmarks/live-suite.json): mathematical reasoning, research, UI/UX, software engineering, artifact production
- [Manual actual-output capture, offline assertions and baseline comparison](engine/live.py)
- [CI readiness workflow](.github/workflows/live-evaluation.yml) verifies suite structure and unit tests.
- Existing [v0.3 intelligence engine](modules/INTELLIGENCE.md) and [module registry](registry/modules.json) remain available.

**Limits:** No live LLM API invocation, automated semantic human grading, executable software artifact tests or binary document rendering are claimed. Capturing supplied real AI responses is supported, and subjective checks stay pending manual independent review. No API key required for offline mode.

## Commands
```bash
python scripts/validate.py
python -m unittest discover -s tests -v
python engine/live.py capture --out run.json --task-id t1 --run-id r1 --arm forge --source-ref response.txt --output response.txt --case-id math-01
python engine/live.py evaluate --suite benchmarks/live-suite.json --run run.json
```

See [v0.4 implementation contract](modules/LIVE_EVALUATION.md).
