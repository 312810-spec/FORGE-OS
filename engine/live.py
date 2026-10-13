#!/usr/bin/env python3
"""FORGE v0.4 real-output capture and offline benchmark runner.

Manual imports are actual supplied output files, NOT claims of live model invocation.
No network, API credentials, implicit model calls, or automatic approval.
"""
import argparse
import hashlib
import json
import pathlib
import re
import sys
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parents[1]
CATEGORIES={"mathematics","research","ui-ux","software","artifact"}
REQUIRED_META={"run_id","task_id","arm","source_kind","source_ref","created_at"}
ARMS={"baseline","forge"}
SOURCE_KINDS={"manual-import","provider-api"}
MAX_BYTES=2_000_000

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def safe_read(path):
    p=pathlib.Path(path)
    if not p.is_file() or p.stat().st_size>MAX_BYTES:
        raise ValueError("Missing or oversized input file")
    return p.read_bytes()

def validate_run(run):
    if not isinstance(run,dict) or not REQUIRED_META.issubset(run):
        raise ValueError("Run missing required metadata")
    if run["arm"] not in ARMS or run["source_kind"] not in SOURCE_KINDS:
        raise ValueError("Invalid run arm/source")
    if not isinstance(run.get("outputs"),list) or not run["outputs"]:
        raise ValueError("Run requires actual captured outputs")
    ids=set()
    for output in run["outputs"]:
        if not isinstance(output,dict) or not isinstance(output.get("case_id"),str) or not isinstance(output.get("text"),str):
            raise ValueError("Invalid captured output")
        if output["case_id"] in ids:
            raise ValueError("Duplicate case output")
        ids.add(output["case_id"])
        if "sha256" not in output or output["sha256"]!=sha256(output["text"].encode("utf-8")):
            raise ValueError("Output checksum mismatch")
    return run

def capture(path, *, task_id, run_id, arm, source_ref, output_path, case_id, model="unknown",
            source_kind="manual-import", instructions_ref="unknown"):
    raw=safe_read(output_path)
    text=raw.decode("utf-8")
    if not text.strip():
        raise ValueError("Empty output")
    record={"run_id":run_id,"task_id":task_id,"arm":arm,
            "source_kind":source_kind,"source_ref":source_ref,
            "instructions_ref":instructions_ref,"model":model,
            "created_at":datetime.now(timezone.utc).isoformat(),
            "outputs":[{"case_id":case_id,"text":text,"sha256":sha256(raw)}]}
    validate_run(record)
    dest=pathlib.Path(path)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(record,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return record

def validate_suite(suite):
    if suite.get("schema_version")!="0.4" or not isinstance(suite.get("cases"),list) or not suite["cases"]:
        raise ValueError("Invalid v0.4 suite")
    ids=set()
    for c in suite["cases"]:
        if c.get("category") not in CATEGORIES or not isinstance(c.get("id"),str) or c["id"] in ids:
            raise ValueError("Invalid/duplicate case")
        ids.add(c["id"])
        checks=c.get("checks",[])
        if not isinstance(checks,list) or not checks:
            raise ValueError("Missing assertions")
        for item in checks:
            if item.get("type") not in ("contains_all","contains_none","regex","exact","manual_review"):
                raise ValueError("Unknown assertion")
            if item["type"]=="regex":
                re.compile(item["pattern"])
    return suite

def run_suite(suite,run):
    validate_suite(suite)
    validate_run(run)
    outputs={o["case_id"]:o["text"] for o in run["outputs"]}
    cases=[]
    for case in suite["cases"]:
        output=outputs.get(case["id"])
        assertions=[]
        for check in case["checks"]:
            if output is None:
                status="fail"
            elif check["type"]=="contains_all":
                status="pass" if all(term in output for term in check["values"]) else "fail"
            elif check["type"]=="contains_none":
                status="pass" if all(term not in output for term in check["values"]) else "fail"
            elif check["type"]=="regex":
                status="pass" if re.search(check["pattern"],output) else "fail"
            elif check["type"]=="exact":
                status="pass" if output.strip()==check["value"] else "fail"
            else:
                status="needs-human-review"
            assertions.append({"type":check["type"],"status":status})
        status="fail" if any(a["status"]=="fail" for a in assertions) else (
            "needs-human-review" if any(a["status"]=="needs-human-review" for a in assertions) else "pass")
        cases.append({"id":case["id"],"category":case["category"],"status":status,"checks":assertions})
    return {"run_id":run["run_id"],"arm":run["arm"],"model":run.get("model","unknown"),
            "source_kind":run["source_kind"],"status":("fail" if any(c["status"]=="fail" for c in cases) else
            "needs-human-review" if any(c["status"]=="needs-human-review" for c in cases) else "pass"),
            "cases":cases,"scope":"offline assertions on captured output; semantic quality requires independent review"}

def compare_runs(suite,baseline,candidate):
    if baseline["task_id"]!=candidate["task_id"] or baseline["arm"]!="baseline" or candidate["arm"]!="forge":
        raise ValueError("Arms or task IDs are incompatible")
    old=run_suite(suite,baseline)
    new=run_suite(suite,candidate)
    a={x["id"]:x["status"] for x in old["cases"]}
    b={x["id"]:x["status"] for x in new["cases"]}
    return {"baseline":old,"candidate":new,
            "improvements":[k for k in a if a[k]=="fail" and b[k]=="pass"],
            "regressions":[k for k in a if a[k]=="pass" and b[k]=="fail"],
            "pending_review":[k for k in b if b[k]=="needs-human-review"],
            "release_gate":"conditional" if new["status"]=="needs-human-review" and not any(a[k]=="pass" and b[k]=="fail" for k in a) else
            "pass" if new["status"]=="pass" and not any(a[k]=="pass" and b[k]=="fail" for k in a) else "fail",
            "comparability":{"task_id_match":True,
                             "model_match":baseline.get("model")==candidate.get("model"),
                             "notes":"Model equality alone does not establish identical settings, context or sampling conditions."},
            "limitations":["Assertions are not independent human-quality ratings","Outputs were imported; no provider run is implied"]}

def main():
    p=argparse.ArgumentParser()
    sub=p.add_subparsers(dest="cmd",required=True)
    c=sub.add_parser("capture")
    for a in ("out","task-id","run-id","arm","source-ref","output","case-id"):
        c.add_argument("--"+a,required=True)
    c.add_argument("--model",default="unknown")
    c.add_argument("--instructions-ref",default="unknown")
    r=sub.add_parser("evaluate")
    r.add_argument("--suite",required=True);r.add_argument("--run",required=True);r.add_argument("--out")
    d=sub.add_parser("compare")
    for a in ("suite","baseline","candidate"):d.add_argument("--"+a,required=True)
    d.add_argument("--out")
    args=p.parse_args()
    if args.cmd=="capture":
        result=capture(args.out,task_id=args.task_id,run_id=args.run_id,arm=args.arm,
                       source_ref=args.source_ref,output_path=args.output,case_id=args.case_id,
                       model=args.model,instructions_ref=args.instructions_ref)
    else:
        suite=json.loads(safe_read(args.suite))
        if args.cmd=="evaluate":result=run_suite(suite,json.loads(safe_read(args.run)))
        else:result=compare_runs(suite,json.loads(safe_read(args.baseline)),json.loads(safe_read(args.candidate)))
        if args.out:
            dest=pathlib.Path(args.out);dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,ensure_ascii=False))
    return 1 if result.get("status",result.get("release_gate"))=="fail" else 0
if __name__=="__main__":
    sys.exit(main())
