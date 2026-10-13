#!/usr/bin/env python3
"""Deterministic repository health report for scheduled Actions; no external credentials."""
import json
import pathlib
import subprocess
import sys
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parents[1]
COMMANDS=[
    [sys.executable,"scripts/validate.py"],
    [sys.executable,"-m","unittest","discover","-s","tests","-v"]
]

def main():
    results=[]
    success=True
    for cmd in COMMANDS:
        run=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,timeout=90,check=False)
        results.append({"command":" ".join(cmd),"exit_code":run.returncode,
                        "stdout":run.stdout[-12000:],"stderr":run.stderr[-12000:]})
        success=success and run.returncode==0
    report={"generated_utc":datetime.now(timezone.utc).isoformat(),
            "status":"pass" if success else "fail","kind":"static-repository-health",
            "results":results,"limitations":["Does not exercise live ChatGPT or external projects",
            "No model evaluation, browser or cloud-agent execution performed"]}
    dest=ROOT/"reports"/"health-latest.json"
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],"report":str(dest.relative_to(ROOT))}))
    return 0 if success else 1
if __name__=="__main__":
    sys.exit(main())
