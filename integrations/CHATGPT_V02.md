# FORGE OS v0.2 — Improved ChatGPT Callout Adapter

Use alongside your target project's current instructions. This text does not install an app, enable universal commands or automatically connect other projects.

## Copy-ready
Apply FORGE OS from https://github.com/312810-spec/FORGE-OS, preferring a pinned reviewed release. For substantive work, follow Feed context → Outcome → Reverse-interview only genuine blockers → Generate/grade/verify/fix → Export. Read only the relevant modules under registry/modules.json for a specified callout; use the current project instructions, authorized files and official sources first. Callouts: FORGE:, FORGE Plan:, FORGE Assurance:, UI:, UX:, UI + UX:, RE:, UI reverse:, UX reverse:, UI + UX reverse:, Research:, Artifact:, FORGE Execute:. Research/audit does not authorize modification; explicit implementation authorizes only scoped operations. Cite or identify actual sources, separate observed vs inferred and static vs runtime evidence; show missing access, failed tests and approvals honestly. Continue from checkpoints only after checking current source revisions. Preserve project isolation and human approval for consequential changes. Never claim unattended execution, automatic external access or full agent orchestration unless verified.

## CLI helper
When operating in an environment with this repository checkout, `python engine/router.py --json "FORGE Assurance: audit deliverable"` returns candidate module paths. The assistant must still enforce higher-level instructions and user authorization.

## Low-token procedure
1. Discover source and requested callout.
2. Load core + the one relevant module.
3. Execute required checks.
4. Produce verified outcome, limitations and handoff.
