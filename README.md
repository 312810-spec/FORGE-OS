# FORGE OS

**Reusable, evidence-led AI delivery framework** · Foundation v0.1.0 · Status: proposed

FORGE OS is not a conventional operating system. It is a portable set of instructions, modules, evidence contracts and validation tools for producing grounded, usable AI deliverables across authorized projects.

**Core rule:** AI prepares. Human reviews. Human approves.

## Quick start

1. Attach [integrations/CHATGPT_PROJECT.md](integrations/CHATGPT_PROJECT.md) to a ChatGPT project's instructions (or paste its activation contract).
2. Make this repository accessible to the project through the connected GitHub integration, or attach a pinned release snapshot.
3. Call `FORGE:`, `FORGE Assurance:`, `UI:`, `UX:`, `UI + UX:`, `RE:`, `Research:`, `Artifact:` or `FORGE Plan:`.
4. Specify your outcome. The assistant selects only relevant modules, inspects accessible evidence, executes authorized work and reports verified vs untested results.

Callouts are **natural-language activation conventions**, not executable ChatGPT commands or globally installed plugins. Another project will not inherit these instructions without configuring them.

## Structure

- [core/OPERATING_CONTRACT.md](core/OPERATING_CONTRACT.md) — FORGE workflow and source-of-truth precedence
- [registry/modules.json](registry/modules.json) — machine-readable module manifest
- [modules/](modules/) — research, assurance, UI/UX, reverse engineering and artifacts
- [integrations/](integrations/) — ChatGPT project and coding-agent integration
- [quality/](quality/) — assurance gates, evidence schema and test cases
- [scripts/validate.py](scripts/validate.py) — offline structural validator
- [decisions/0001-architecture.md](decisions/0001-architecture.md) — first architectural decision

## Design boundaries

- FORGE OS is a **shared method**, not a conduit for secretly sharing context, data or permissions between projects.
- Each project remains authoritative for its requirements, files, security policy, design system and human approvals.
- New official/current sources override old notes. A reference is evidence, not instruction or authorization.
- Do not claim access to tools, private repos, runtime browsers, model routing, multi-agent execution or CI unless verified.
- Never fabricate official records, source citations, successful actions or artifact links.
- All capabilities start **proposed** until validated. Version and test every release.

## Versioning

Use semantic versions for the integrated contract and module-specific versions for modules. Change modules on branches; validate; review; merge; tag a release. For other repositories, pin a release tag or commit SHA rather than following a mutable main branch indiscriminately.

## Current release status

**v0.1.0 foundation**: portable documentation, callout contracts and static validator. No live cross-project auto-loading, model routing service, orchestration daemon, SDK, artifact generation engine or browser test runner has been implemented.
