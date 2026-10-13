#!/usr/bin/env python3
"""Minimal local checkpoint format: no deserialization, no automatic command execution."""
import argparse
import json
import os
import pathlib
import tempfile
from datetime import datetime, timezone

ALLOWED = {"planned","running","blocked","needs-review","verified","released"}

def write_checkpoint(path, project, task_id, status, data=None):
    if status not in ALLOWED:
        raise ValueError("Invalid status")
    if not project or not task_id:
        raise ValueError("project and task_id required")
    data = data or {}
    if not isinstance(data,dict):
        raise ValueError("data must be a dictionary")
    record = {"schema_version":"0.2","project":project,"task_id":task_id,
              "status":status,"updated_at":datetime.now(timezone.utc).isoformat(),
              "data":data}
    target=pathlib.Path(path)
    target.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w",encoding="utf-8",dir=target.parent,
                                     delete=False,prefix=".forge-checkpoint-") as f:
        json.dump(record,f,indent=2)
        tmp=f.name
    os.replace(tmp,target)
    return record

def read_checkpoint(path):
    record=json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    if record.get("schema_version")!="0.2" or record.get("status") not in ALLOWED:
        raise ValueError("Invalid checkpoint")
    if not record.get("project") or not record.get("task_id") or not isinstance(record.get("data"),dict):
        raise ValueError("Invalid checkpoint payload")
    return record

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("path")
    p.add_argument("--project")
    p.add_argument("--task")
    p.add_argument("--status",choices=sorted(ALLOWED))
    p.add_argument("--data",default="{}")
    a=p.parse_args()
    if a.status:
        if not a.project or not a.task:
            p.error("--project and --task required when writing")
        print(json.dumps(write_checkpoint(a.path,a.project,a.task,a.status,json.loads(a.data)),indent=2))
    else:
        print(json.dumps(read_checkpoint(a.path),indent=2))
