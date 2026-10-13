#!/usr/bin/env python3
"""Offline evidence-based benchmark evaluator, no LLM calls or network.

Suite case contracts:
- output_equal: literal expected text comparison
- contains_all: required substrings
- contains_none: forbidden substrings
- status_equal: exact status
- require_evidence: nonempty evidence list and a declared source
The record is an externally supplied candidate/baseline result, not a generated answer.
"""
import argparse
import json
from pathlib import Path

CHECKS={"output_equal","contains_all","contains_none","status_equal","require_evidence"}

def evaluate_case(case, result):
    details=[]
    for assertion in case["assertions"]:
        kind=assertion["type"]
        if kind not in CHECKS:
            raise ValueError("Unknown assertion type: "+kind)
        if kind=="output_equal":
            passed=result.get("output")==assertion["value"]
        elif kind=="contains_all":
            passed=isinstance(result.get("output"),str) and all(s in result["output"] for s in assertion["values"])
        elif kind=="contains_none":
            passed=isinstance(result.get("output"),str) and all(s not in result["output"] for s in assertion["values"])
        elif kind=="status_equal":
            passed=result.get("status")==assertion["value"]
        else:
            passed=isinstance(result.get("evidence"),list) and len(result["evidence"])>0 and all(
                isinstance(e,dict) and bool(e.get("source")) and bool(e.get("observation"))
                for e in result["evidence"])
        details.append({"type":kind,"passed":passed})
    return {"id":case["id"],"passed":all(x["passed"] for x in details),"checks":details}

def evaluate(suite, results):
    if not isinstance(suite.get("cases"),list) or not suite["cases"]:
        raise ValueError("No benchmark cases")
    ids=[c["id"] for c in suite["cases"]]
    if len(ids)!=len(set(ids)):
        raise ValueError("Duplicate case ID")
    records=results.get("results")
    if not isinstance(records,list) or any(not isinstance(r,dict) or "id" not in r for r in records):
        raise ValueError("Invalid results")
    result_ids=[r["id"] for r in records]
    if len(result_ids)!=len(set(result_ids)) or set(result_ids)-set(ids):
        raise ValueError("Duplicate or unknown result ID")
    by_id={r["id"]:r for r in records}
    cases=[]
    for case in suite["cases"]:
        cases.append(evaluate_case(case,by_id[case["id"]]) if case["id"] in by_id else
                     {"id":case["id"],"passed":False,"checks":[],"error":"missing result"})
    passed=sum(1 for c in cases if c["passed"])
    return {"suite":suite.get("id","unnamed"),"status":"pass" if passed==len(cases) else "fail",
            "passed":passed,"total":len(cases),"cases":cases,
            "scope":"deterministic offline assertions; not evidence of live model quality"}

def compare(suite, baseline, candidate):
    old=evaluate(suite,baseline)
    new=evaluate(suite,candidate)
    before={c["id"]:c["passed"] for c in old["cases"]}
    after={c["id"]:c["passed"] for c in new["cases"]}
    return {"baseline":old,"candidate":new,
            "improvements":[k for k in before if not before[k] and after[k]],
            "regressions":[k for k in before if before[k] and not after[k]],
            "unchanged":[k for k in before if before[k]==after[k]],
            "release_gate":"pass" if new["status"]=="pass" and not any(before[k] and not after[k] for k in before) else "fail"}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--suite",required=True)
    p.add_argument("--candidate",required=True)
    p.add_argument("--baseline")
    p.add_argument("--out")
    args=p.parse_args()
    suite=json.loads(Path(args.suite).read_text(encoding="utf-8"))
    candidate=json.loads(Path(args.candidate).read_text(encoding="utf-8"))
    answer=compare(suite,json.loads(Path(args.baseline).read_text(encoding="utf-8")),candidate) if args.baseline else evaluate(suite,candidate)
    serialized=json.dumps(answer,indent=2,ensure_ascii=False)+"\n"
    if args.out:
        Path(args.out).parent.mkdir(parents=True,exist_ok=True)
        Path(args.out).write_text(serialized,encoding="utf-8")
    print(serialized)
    return 0 if (answer.get("release_gate",answer.get("status"))=="pass") else 1

if __name__=="__main__":
    raise SystemExit(main())
