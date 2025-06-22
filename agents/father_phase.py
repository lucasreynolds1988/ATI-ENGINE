# ~/Soap/agents/father_phase.py

import json
from pathlib import Path
import time
import os

QUEUE_DIR = Path.home() / "Soap/agent_queue"
os.makedirs(QUEUE_DIR, exist_ok=True)

def validate_logic(sop):
    issues = []

    if not sop.get("tools"):
        issues.append("Missing tool list.")

    if not sop.get("procedure") or not isinstance(sop["procedure"], list):
        issues.append("Procedure is missing or not a list.")
    else:
        for i, step in enumerate(sop["procedure"]):
            if not any(verb in step.lower() for verb in ["install", "remove", "check", "clean", "torque", "grease"]):
                issues.append(f"Step {i+1} may lack a clear action: '{step}'")

    return issues

def run_father():
    tasks = sorted(QUEUE_DIR.glob("*.json"))
    for task in tasks:
        with open(task, "r") as f:
            data = json.load(f)

        if data.get("status") != "watson_complete":
            continue

        print(f"🛠️ Father processing: {task.name}")
        issues = validate_logic(data)

        if issues:
            data["logic_issues"] = issues
            data["status"] = "needs_human_review"
            print(f"⚠️ Logic issues found in {task.name}: {issues}")
        else:
            data["status"] = "father_complete"
            print(f"✅ Logic validated for {task.name}")

        with open(task, "w") as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    run_father()
