# ADR-0001 — Repository as a portable framework

Date: 2026-10-13
Status: proposed

## Decision
Maintain FORGE OS as versioned modular instructions, evidence contracts, test fixtures and integration adapters. A manifest selects relevant modules; target project requirements remain sovereign. Provide a small stdlib validator first.

## Why
A GitHub URL alone cannot inject instructions, tools, memory or permissions into unrelated ChatGPT projects. Modular/pinned retrieval reduces context costs and uncontrolled cross-project carryover.

## Tradeoffs
Readable markdown contracts enable immediate adoption but do not enforce behavior by themselves. Runtime observability, richer CI, agent adapters and automatic retrieval require separate implementation and supported connectors.

## Risks
Drift between project instructions and modules; stale module pins; overclaiming verification; copying confidential project data. Mitigate using explicit version pins, source hierarchy, test cases and human release gates.

## Follow-up
Execute smoke cases, add provenance logs and validated adapters, document release/tag policy, and benchmark quality against a baseline before marking modules tested/adopted.
