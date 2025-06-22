# ~/Soap/agents/mother_phase.py

import json
from pathlib import Path
import time
import os

QUEUE_DIR = Path.home() / "Soap/agent_queue"
os.makedirs(QUEUE_DIR, exist_ok=True)

PPE_DEFAULTS = [
    "Wear safety glasses.",
    "Use mechanic gloves.",
    "Ensure work area is clean and dry."
]

HAZARD_FLAGS = [
    ("brake", "⚠️ Brake dust may contain asbestos. Avoid blowing or dry brushing."),
    ("jack", "⚠️ Always use jack stands. Never rely solely on a jack."),
    ("grease", "⚠️ Use nitrile gloves to avoid chemical exposure."),
    ("cotter pin", "⚠️ Watch for sharp edges when removing retaining hardware.")
]

def apply_safety(sop):
    added = []

    if "safety" not in sop or not isinstance(sop["safety"], list):
        sop["safety"] = []

    for rule in PPE_DEFAULTS:
        if rule not in sop["safety"]:
            sop["safety"].append(rule)
            added.append(rule)

    for step in sop.get("procedure", []):
        for keyword, warning in HAZARD_FLAGS:
            if keyword in step.lower() and warning not in sop["safety"]:
                sop["safety"].append(warning)
                added.append(warning)

    return added

def run_mother():
    tasks = sorted(QUEUE_DIR.glob("*.json"))
    for task in tasks:
        with open(task, "r") as f:
            data = json.load(f)

        if data.get("status") != "father_complete":
            continue

        print(f"🛡️ Mother processing: {task.name}")
        new_safety = apply_safety(data)

        if new_safety:
            print(f"✅ Added safety to {task.name}: {new_safety}")
        else:
            print(f"🧼 No additional safety needed for {task.name}")

        data["status"] = "mother_complete"

        with open(task, "w") as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    run_mother()
