# FORGE Orchestration v0.1.0

**Callout:** `FORGE Execute: [authorized task]`.

1. Inventory accessible tools, limits, source provenance, costs, required permissions and environment.
2. Choose the smallest capable execution plan and independent verification checks.
3. Route to relevant modules; do not run every module by default.
4. Parallelize only independent and supported tasks with bounded resource and budget usage.
5. Prefer read-only inspection, branch-first edits, clean commits and CI. Reserve irreversible or cross-project operations for authorized scope.
6. After a tool failure, record error, bounded retry and fallback route. Static inspection cannot stand in for browser testing.
7. Record actions actually executed, artifacts changed, test commands/results and remaining gaps.
8. Never suggest that specifying a model or multiple agents grants access that the runtime does not provide.

Proposed orchestration guidance only; no autonomous daemon, background task service or multi-model router is installed.
