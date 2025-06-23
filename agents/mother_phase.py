#!/usr/bin/env python3
"""
mother_phase.py: Safety conscience for ATI SOP system.
Appends PPE defaults and hazard-specific warnings to SOPs.
"""
import json
import logging
from pathlib import Path

# Configuration
HOME_DIR = Path.home()
QUEUE_DIR = HOME_DIR / "Soap" / "agent_queue"
LOG_DIR = HOME_DIR / "Soap" / "data" / "logs"
LOG_FILE = LOG_DIR / "mother_phase.log"

# Default safety rules
PPE_DEFAULTS = [
    "Wear safety glasses.",
    "Use mechanic gloves.",
    "Ensure work area is clean and dry."
]
# Keyword-based hazard flags
HAZARD_FLAGS = [
    ("brake", "⚠️ Brake dust may contain asbestos. Avoid blowing or dry brushing."),
    ("jack", "⚠️ Always use jack stands. Never rely solely on a jack."),
    ("grease", "⚠️ Use nitrile gloves to avoid chemical exposure."),
    ("cotter pin", "⚠️ Watch for sharp edges when removing retaining hardware.")
]

# Setup logging
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger()

def log(message, level=logging.INFO):
    print(message)
    logger.log(level, message)


def apply_safety(sop: dict) -> list:
    """Append default PPE and hazard warnings to SOP data."""
    added = []
    sop.setdefault("safety", [])
    # Add PPE defaults
    for rule in PPE_DEFAULTS:
        if rule not in sop["safety"]:
            sop["safety"].append(rule)
            added.append(rule)
    # Add hazard-specific flags
    for step in sop.get("procedure", []):
        for keyword, warning in HAZARD_FLAGS:
            if keyword in step.lower() and warning not in sop["safety"]:
                sop["safety"].append(warning)
                added.append(warning)
    return added


def run_mother():
    tasks = sorted(QUEUE_DIR.glob("*.json"))
    for task in tasks:
        try:
            data = json.loads(task.read_text())
            if data.get("status") != "father_complete":
                continue
            log(f"🛡️ Mother processing: {task.name}")
            # Backup before changes
            data["mother_backup"] = json.loads(json.dumps(data))
            new_rules = apply_safety(data)
            if new_rules:
                log(f"✅ Added safety rules for {task.name}: {new_rules}")
            else:
                log(f"🧼 No new safety rules needed for {task.name}")
            data["status"] = "mother_complete"
            task.write_text(json.dumps(data, indent=2))
        except Exception as e:
            log(f"❌ Mother error on {task.name}: {e}", level=logging.ERROR)


if __name__ == "__main__":
    run_mother()
