"""Deterministic capability/cost selector; plans only, never calls model APIs."""
import json
from pathlib import Path

CATALOG=Path(__file__).resolve().parents[1]/"registry"/"providers.json"

def select(requirements, catalog_path=CATALOG):
    data=json.loads(Path(catalog_path).read_text(encoding="utf-8"))
    required=set(requirements.get("capabilities",[]))
    budget=requirements.get("max_cost_per_million_output_tokens")
    if budget is not None and (isinstance(budget,bool) or not isinstance(budget,(int,float)) or budget<0):
        raise ValueError("Invalid budget")
    candidates=[]
    for item in data["providers"]:
        if not item["enabled"] or not required.issubset(item["capabilities"]):
            continue
        cost=item.get("cost_per_million_output_tokens")
        if budget is not None and (cost is None or cost>budget):
            continue
        candidates.append(item)
    candidates.sort(key=lambda item:(item.get("cost_per_million_output_tokens") is None,
                                    float("inf") if item.get("cost_per_million_output_tokens") is None else item["cost_per_million_output_tokens"],item["id"]))
    return {"status":"selected" if candidates else "unavailable",
            "candidate":candidates[0]["id"] if candidates else None,
            "eligible":[item["id"] for item in candidates],
            "executed":False,"note":"Catalog planning only; verify entitlement, tool permissions and current pricing before actual usage."}
