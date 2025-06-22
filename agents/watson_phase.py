# ~/Soap/agents/watson_phase.py

import json
from pathlib import Path
import time
import os

QUEUE_DIR = Path.home() / "Soap/agent_queue"
os.makedirs(QUEUE_DIR, exist_ok=True)

def structure_sop(raw_text):
    structured = {
        "title": "Auto SOP - Watson Structured",
        "purpose": "Describe the purpose of this SOP.",
        "scope": "Covers the procedure for the specified system.",
        "tools": ["Tool A", "Tool B"],
        "materials": ["Material X"],
        "safety": ["Wear PPE", "Disconnect power source"],
        "procedure": [
            "Step 1: Begin safely.",
            "Step 2: Follow diagnostic flow.",
            "Step 3: Complete all checks."
        ]
    }
    structured["watson_backup"] = json.loads(json.dumps(structured))  # Deep copy snapshot
    return structured

def run_watson():
    tasks = sorted(QUEUE_DIR.glob("*.json"))
    for task in tasks:
        with open(task, "r") as f:
            data = json.load(f)

        if data.get("status") != "queued":
            continue

        print(f"🧠 Watson processing: {task.name}")
        structured = structure_sop(data.get("raw_text", ""))

        data.update(structured)
        data["status"] = "watson_complete"

        with open(task, "w") as f:
            json.dump(data, f, indent=2)

        print(f"✅ Watson complete: {task.name}")

if __name__ == "__main__":
    run_watson()
