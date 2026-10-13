# FORGE Assurance v0.1.0

**Callout:** `FORGE Assurance: Audit [deliverable] against [outcome, requirements, sources].`

Inspection only by default; do not alter the deliverable without implementation authorization.

1. Identify intended users, task, source hierarchy, acceptance contract and consequential failure modes.
2. Gather accessible artifact/repository/source evidence. Explicitly identify unavailable or outdated material.
3. Evaluate grounding/provenance, correctness, coverage, internal consistency, accessibility, editability, usability, presentation, safety/privacy and maintainability as applicable.
4. Run independent checks: computations, citations, structured schemas, answer keys, tests, link integrity, render/overflow and live journeys where available.
5. For each finding: ID, severity (critical/high/medium/low), location, evidence, user impact, likely cause, recommended fix and verification step.
6. Distinguish **verified defect**, **risk/recommendation**, **unknown/untested**. No unsupported numeric perfection scores.
7. If implementation authorized, fix by severity, retest regressions, provide concise before/after evidence and pending limitations.
8. Report gate: `pass`, `conditional`, `fail` or `not evaluated`, with reasons. Human approval remains separate from passing checks.

See `quality/GATES.md` and `quality/EVIDENCE_SCHEMA.json`.
