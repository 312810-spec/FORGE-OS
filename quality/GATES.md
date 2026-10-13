# FORGE Release Gates v0.1.0

Apply proportional gates. A documentation change need not require full browser QA; an interactive UI or critical assessment does.

| Gate | Evidence | Failure action |
| --- | --- | --- |
| Context | Current authoritative requirements identified | Mark missing and block unsupported assertions |
| Grounding | Claims tied to accessible sources | Remove/qualify unsupported claims |
| Correctness | Calculations, tests, schemas, or sample outputs checked | Fix and rerun |
| Completeness | Outcome/acceptance checklist addressed | Complete or mark exceptions |
| Usability | Audience can perform intended task | Revise flow and verify |
| Accessibility | Relevant keyboard, focus, contrast and semantics checks | Fix or record risk |
| Artifact integrity | File opens/parses; editing/rendering checked as needed | Regenerate/repair |
| Security/privacy | No secrets/leaks/unauthorized copying | Stop and remediate |
| Runtime | Live workflow confirmed when claim depends on it | Mark untested, never invent |
| Release | Diff reviewed, CI/gates checked, human approval as required | Keep branch/PR open |

Final outcomes: PASS (all mandatory checks passed), CONDITIONAL (clearly scoped limitations accepted), FAIL (mandatory check fails), NOT EVALUATED (no evidence).
