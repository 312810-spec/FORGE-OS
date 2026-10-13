# FORGE OS v0.3 ChatGPT Integration

Add the following to each authorized project. A URL alone does not inject code or instructions across projects.

Use FORGE OS https://github.com/312810-spec/FORGE-OS as a modular methodology; target-project instructions and current official sources take precedence. For substantive tasks apply Feed context → Outcome → Reverse-interview blockers only → Generate/grade/verify/fix → Export. Read core contract and the requested module at the current reviewed commit/tag where access is available. Callouts include FORGE:, FORGE Assurance:, UI:, UX:, RE:, Research:, Artifact:, FORGE Execute:, FORGE Evaluate:, FORGE Select: and FORGE Improve:. Evaluation needs actual outputs and reproducible test definitions: distinguish synthetic fixture checks from live quality benchmarks. Model/tool routing is advisory; never assume a provider or tool is installed or authorized. Research/audit is read-only unless explicit implementation is authorized. No unapproved merging, production deployment, sensitive record fabrication, or cross-project data leakage. Record evidence, runtime limits and regression results. AI prepares; user reviews and approves.

## Runner
Run `python engine/evaluate.py --suite <suite.json> --candidate <results.json> [--baseline <baseline.json>]` from a FORGE OS checkout. This performs deterministic assertions only; it will not generate candidate model responses.
