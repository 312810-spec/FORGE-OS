# FORGE Continuity and Checkpoint Contract v0.2.0

Inspired by LangGraph and Microsoft Agent Framework checkpoint/resume patterns, without installing either runtime.

The optional `engine/checkpoint.py` utility persists a small JSON state file locally using an atomic replace. It does **not** execute tasks, sync to GitHub, resume AI thinking, or run asynchronously.

A checkpoint must carry: project/task ID, current state, source revisions, completed actions/evidence, blockers, pending tests, and next authorized action. Do **not** store raw credentials, protected learner information, private tool output, or unrestricted chat transcripts. The `data` field is not automatically sanitized: operators must omit sensitive values.

States: planned → running → blocked / needs-review / verified → released. These are descriptive, not a hardcoded transition graph. Released requires evidence of actual approval and release.

On continuation: reload checkpoint, compare it with current authoritative project files and Git state, invalidate stale findings, then perform only authorized pending actions. The checkpoint cannot outrank current instructions or live source evidence.

Sample: `python engine/checkpoint.py .forge/status.json --project sample --task audit-12 --status blocked --data '{"reason":"browser unavailable"}'`

For durable concurrent/production workflows, design a proper transactional checkpoint store and task identity policy; the current JSON utility is local single-writer only.
