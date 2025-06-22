# ~/Soap/agents/arbiter_phase.py

import json
from pathlib import Path
import hashlib
import os
from arbiter_knowledge import resolve_conflict

QUEUE_DIR = Path.home() / "Soap/agent_queue"
os.makedirs(QUEUE_DIR, exist_ok=True)

def hash_field(value):
    if isinstance(value, list):
        value = "\n".join(value)
    elif isinstance(value, dict):
        value = json.dumps(value, sort_keys=True)
    elif not isinstance(value, str):
        value = str(value)
    return hashlib.md5(value.encode()).hexdigest()

def detect_conflict(watson, father, mother):
    fields = ["procedure", "safety", "tools", "materials"]
    conflicts = []

    for field in fields:
        w_hash = hash_field(watson.get(field, ""))
        f_hash = hash_field(father.get(field, ""))
        m_hash = hash_field(mother.get(field, ""))

        if not (w_hash == f_hash == m_hash):
            conflicts.append(field)

    return conflicts

def run_arbiter():
    tasks = sorted(QUEUE_DIR.glob("*.json"))
    for task in tasks:
        with open(task, "r") as f:
            data = json.load(f)

        if data.get("status") != "mother_complete":
            continue

        print(f"⚖️ Arbiter reviewing: {task.name}")
        conflicts = detect_conflict(
            data.get("watson_backup", {}),
            data.get("father_backup", {}),
            data.get("mother_backup", {})
        )

        if not conflicts:
            data["status"] = "fully_verified"
            print(f"✅ Consensus achieved: {task.name}")
        else:
            print(f"🚨 Conflicts found: {conflicts}")
            resolution, context = resolve_conflict(data)

            if resolution == "resolved":
                data["status"] = "fully_verified"
                data["arbiter_notes"] = ["Logic rules passed on re-check."]
                print(f"✅ Resolved via logic.")
            elif resolution.startswith("reference_found"):
                data["status"] = "fully_verified"
                data["arbiter_notes"] = [f"Resolved by reference: {context}"]
                print(f"📚 Verified with external source.")
            else:
                data["status"] = "needs_human_review"
                data["conflict_fields"] = conflicts
                data["arbiter_notes"] = [f"Unresolved issues: {context}"]
                print(f"🛑 Needs human review.")

        with open(task, "w") as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    run_arbiter()
