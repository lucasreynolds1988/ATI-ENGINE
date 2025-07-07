# ~/Soap/sop_admin_review.py

"""
Admin Review Agent — Flags conflicts, logs summary, allows human approval cycle.
"""

import json
from pathlib import Path
from datetime import datetime

QUEUE_DIR = Path.home() / "Soap/agent_queue"
LOG_FILE = Path.home() / "Soap/logs/admin_review.log"
QUEUE_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def load_latest_sop():
    path = QUEUE_DIR / "latest_sop.json"
    if not path.exists():
        return None, "❌ No SOP found in queue"
    with open(path, "r") as f:
        try:
            return json.load(f), None
        except Exception as e:
            return None, f"❌ Failed to parse SOP: {str(e)}"

def log_review(sop):
    with open(LOG_FILE, "a") as f:
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conflicts = sop.get("conflicts", [])
        f.write(f"[{ts}] TITLE: {sop.get('title','N/A')} | STATUS: {sop.get('status','pending')} | CONFLICTS: {len(conflicts)}\n")

def perform_review(sop):
    conflict_count = len(sop.get("conflicts", []))
    status = "pending" if conflict_count else "approved"
    sop["status"] = status
    log_review(sop)
    with open(QUEUE_DIR / "latest_sop.json", "w") as f:
        json.dump(sop, f, indent=2)
    return f"✅ SOP reviewed: {status.upper()} ({conflict_count} conflicts)"

def main():
    sop, error = load_latest_sop()
    if error:
        print(json.dumps({"error": error}))
        return
    result = perform_review(sop)
    print(json.dumps({"result": result}))

if __name__ == "__main__":
    main()
