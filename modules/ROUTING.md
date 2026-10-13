# FORGE Router v0.2.0 — Improved Callouts

## Behavior
The callable interface has **two layers**:
1. The assistant reads the user request and applicable project authority.
2. A deterministic optional CLI `engine/router.py` maps **prefixes** to versioned modules and identifies provisional read/change intent.

This CLI never grants permission, invokes models, reads other projects, or runs tools. The assistant must inspect accessible relevant files, enforce authorization and adapt the process to the outcome.

## Main callouts
| Callout | Module | Purpose |
| --- | --- | --- |
| FORGE: | core | End-to-end FORGE |
| FORGE Plan: | core | Outcome and plan |
| FORGE Assurance: | assurance | Evidence-driven audit |
| UI: / UX: / UI + UX: | ui-ux | Review/design/implement when authorized |
| RE: / UI reverse: / UX reverse: / UI + UX reverse: | reverse-engineering | Lawful reference analysis |
| Research: | research | Fresh primary-source investigation |
| Artifact: | artifacts | Artifact creation and validation |
| FORGE Execute: | orchestration | Tool routing and implementation |

## Improved call syntax
`FORGE Assurance: [artifact]. Outcome: [goal]. Sources: [locations]. Mode: audit only.`
`RE: [url]. Inspect: [feature]. Deliver: spec + evidence + adaptation. Mode: research only.`
`FORGE Execute: [repository task]. Gates: [tests]. Approval: [boundary].`

## CLI
`python engine/router.py --json "UI + UX reverse: inspect onboarding"`

The route result lists module files and a *provisional* intent. Check repository state, tools, user instructions and source precedence before any action. `requires_approval` is a warning flag, not an authorization authority. Missing prefixes remain unmatched to avoid unnecessary context loading.

## Future extension
Add schema-validated module capabilities, dependency graphs, provider adapters and safe read-only registry discovery. Do not silently infer access to models, tools or plugins.
