#!/usr/bin/env python3
"""Offline FORGE OS manifest + documentation validator (stdlib only)."""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REQUIRED = ["README.md", "core/OPERATING_CONTRACT.md", "registry/modules.json",
            "integrations/CHATGPT_PROJECT.md", "quality/GATES.md",
            "quality/EVIDENCE_SCHEMA.json"]
errors = []
for name in REQUIRED:
    if not (ROOT / name).is_file():
        errors.append(f"Missing required file: {name}")
try:
    manifest = json.loads((ROOT / "registry/modules.json").read_text(encoding="utf-8"))
    seen_ids, seen_triggers = set(), set()
    for module in manifest["modules"]:
        mid = module["id"]
        if mid in seen_ids:
            errors.append(f"Duplicate module: {mid}")
        seen_ids.add(mid)
        if not (ROOT / module["path"]).is_file():
            errors.append(f"Missing module path: {module['path']}")
        for trigger in module["triggers"]:
            if trigger in seen_triggers:
                errors.append(f"Duplicate activation trigger: {trigger}")
            seen_triggers.add(trigger)
    schema = json.loads((ROOT / "quality/EVIDENCE_SCHEMA.json").read_text(encoding="utf-8"))
    assert schema["type"] == "object"
except (OSError, ValueError, KeyError, AssertionError) as exc:
    errors.append(f"Invalid manifest/schema: {exc}")
if errors:
    for error in errors:
        print("FAIL:", error, file=sys.stderr)
    sys.exit(1)
print(f"PASS: {len(REQUIRED)} required paths, {len(seen_ids)} modules, {len(seen_triggers)} unique callouts.")
