# FORGE OS

**Reusable, evidence-led AI delivery framework** · v0.2.0 candidate · Status: static tooling under validation

FORGE OS is not a conventional operating system. It is a modular, version-controlled methodology plus lightweight tools for better AI deliverables, grounded in evidence and human approval.

**Core rule:** AI prepares. Human reviews. Human approves.

## Quick start
- In ChatGPT, use [v0.2 project adapter](integrations/CHATGPT_V02.md) and configure access to a pinned FORGE-OS release.
- Call `FORGE:`, `FORGE Assurance:`, `UI + UX:`, `RE:`, `Research:`, `Artifact:` or `FORGE Execute:`.
- In a checkout, try `python engine/router.py --json "RE: inspect tabs"` to route to a module.
- Run `python scripts/health_report.py` for deterministic tests and a machine-readable report.

## What v0.2 adds
- [Versioned callable-module router](modules/ROUTING.md) with tested lexical routing. A route is **not** permission to act.
- [Checkpoint contract and utility](modules/CHECKPOINTS.md) for preserving non-sensitive local task state.
- [Research cross-reference](research/V0.2-CROSS-REFERENCE.md) covering LangGraph, Microsoft Agent Framework, OpenAI Agents SDK, Promptfoo, MCP and agent methodology.
- [Weekly GitHub Actions health](.github/workflows/health.yml), manual dispatch and downloadable test evidence; no external credentials needed.
- [Focused tests](tests/test_router.py), a reusable assurance release gate and clearer integration boundaries.

## Documentation
- [FORGE Core](core/OPERATING_CONTRACT.md)
- [Module registry](registry/modules.json)
- [Assurance](modules/ASSURANCE.md)
- [UI/UX](modules/UI_UX.md)
- [Reverse Engineering](modules/REVERSE_ENGINEERING.md)
- [Research](modules/RESEARCH.md)
- [Artifact production](modules/ARTIFACTS.md)
- [Orchestration](modules/ORCHESTRATION.md)
- [v0.2 integration](integrations/CHATGPT_V02.md)

**Boundaries:** ChatGPT callouts are conventions, not globally registered native commands. The router does not operate models or external tools. CI is static/testing automation, not a running autonomous AI agent. Newest authoritative project evidence always overrides stale handoffs; no confidential cross-project data sharing.

Quality progression: proposed → source-inspected → static-tested → runtime-tested → adopted. Only mark actual checks complete.
