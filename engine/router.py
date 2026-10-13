#!/usr/bin/env python3
"""Deterministic FORGE module routing. No model API, no network, no execution."""
import argparse
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "registry" / "modules.json"

def load_registry(path=MANIFEST):
    data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    ids = set()
    triggers = []
    for module in data["modules"]:
        if module["id"] in ids:
            raise ValueError("Duplicate module id")
        ids.add(module["id"])
        for trigger in module["triggers"]:
            if (trigger.lower(), module["id"]) in triggers:
                raise ValueError("Duplicate trigger")
            triggers.append((trigger.lower(), module["id"]))
    # Longest match wins for nested names; ambiguous equal-length matches fail closed.
    return data, sorted(triggers, key=lambda entry: -len(entry[0]))

def route(prompt, registry_path=MANIFEST):
    registry, triggers = load_registry(registry_path)
    stripped = prompt.lstrip()
    lowered = stripped.lower()
    matched = [(trigger, module_id) for trigger, module_id in triggers
               if lowered.startswith(trigger) and
               (len(lowered) == len(trigger) or lowered[len(trigger)].isspace())]
    if not matched:
        # No silent inference or unwanted module fanout.
        return {"status":"unmatched","modules":[],"intent":"unspecified",
                "requires_approval":False,"reason":"No known callout prefix"}
    best = len(matched[0][0])
    top = [(trigger,module_id) for trigger,module_id in matched if len(trigger)==best]
    if len(set(module_id for _,module_id in top)) != 1:
        return {"status":"ambiguous","modules":[],"intent":"unspecified",
                "requires_approval":True,"reason":"Conflicting equally specific triggers"}
    trigger,module_id = top[0]
    tail = stripped[len(trigger):].strip()
    # Audit and reverse-engineering calls do not authorize mutation on their own.
    write_verbs = re.compile(r"\b(implement|fix|modify|edit|build|create|merge|deploy|delete|publish|commit|integrate)\b",re.I)
    inspect_verbs = re.compile(r"\b(audit|review|inspect|research|analy[sz]e|assess|study)\b",re.I)
    inspect_only = module_id in ("assurance","reverse-engineering") or bool(inspect_verbs.search(tail))
    mutation = bool(write_verbs.search(tail))
    # A request containing both review + implementation is not automatically approval.
    intent = "mixed-review-and-change" if mutation and inspect_only else ("change-requested" if mutation else "read-only")
    requires_approval = bool(mutation and any(x in tail.lower() for x in ("delete", "deploy", "publish", "production", "merge")))
    by_id = {m["id"]:m for m in registry["modules"]}
    selected = [by_id[module_id]]
    if module_id != "core":
        selected.insert(0,by_id["core"])
    return {"status":"routed","trigger":trigger,"modules":[{"id":m["id"],"path":m["path"],
          "version":m["version"]} for m in selected],"intent":intent,
          "requires_approval":requires_approval,
          "reason":"Lexical routing only; actual user authorization and system policy override classification"}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("prompt", nargs="?")
    p.add_argument("--registry", default=str(MANIFEST))
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    if not args.prompt:
        p.error("Provide a callout prompt")
    result = route(args.prompt,args.registry)
    print(json.dumps(result,indent=2,ensure_ascii=False) if args.json else
          f"{result['status']}: {', '.join(x['id'] for x in result['modules']) or '-'} | {result['intent']}")
if __name__ == "__main__":
    main()
