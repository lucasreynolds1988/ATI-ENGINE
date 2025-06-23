# ~/Soap/agents/sop_admin_review.py

import json
from pathlib import Path
import os
import shutil

QUEUE_DIR = Path.home() / "Soap/agent_queue"
APPROVED_DIR = Path.home() / "Soap/sop_storage/approved"
REJECTED_DIR = Path.home() / "Soap/sop_storage/rejected"
LOG_PATH = Path.home() / "Soap/data/rejection_log.json"

os.makedirs(APPROVED_DIR, exist_ok=True)
os.makedirs(REJECTED_DIR, exist_ok=True)
os.makedirs(LOG_PATH.parent, exist_ok=True)

def load_log():
    if LOG_PATH.exists():
        with open(LOG_PATH, "r") as f:
            return json.load(f)
    return []

def save_log(log):
    with open(LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)

def review_sops():
    log = load_log()
    tasks = sorted(QUEUE_DIR.glob("*.json"))

    for task in tasks:
        with open(task, "r") as f:
            data = json.load(f)

        if data.get("status") != "needs_admin_review":
            continue

        print(f"🧾 Reviewing SOP: {task.name}")

        print("\n--- SOP CONTENT ---")
        for step in data.get("procedure", []):
            print("  ✅", step)
        print("\nConflicts:")
        for issue in data.get("conflict_fields", []):
            print("  ⚠️", issue)
        print("-------------------\n")

        decision = input("Approve this SOP? (y/n): ").strip().lower()

        if decision == "y":
            data["status"] = "approved"
            dest = APPROVED_DIR / task.name
            shutil.move(str(task), dest)
            print(f"✅ Moved to: {dest}")

        else:
            data["status"] = "rejected"
            reason = input("Why is this SOP rejected? ")
            mfg = {
                "name": input("MFG Name: "),
                "model": input("MFG Model: "),
                "year": input("MFG Year: ")
            }
            entry = {
                "filename": task.name,
                "reason": reason,
                "mfg": mfg,
                "timestamp": str(Path(task).stat().st_mtime)
            }
            log.append(entry)
            dest = REJECTED_DIR / task.name
            shutil.move(str(task), dest)
            print(f"❌ Moved to: {dest} and logged rejection")

    save_log(log)

if __name__ == "__main__":
    review_sops()
