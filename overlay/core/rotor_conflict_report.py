import os
from core.rotor_overlay import log_event

CONFLICT_LOG = "/home/lucasreynolds1988/Soap/logs/arbiter_conflicts.log"

def report_conflicts():
    if not os.path.isfile(CONFLICT_LOG):
        print("No conflicts found.")
        return
    with open(CONFLICT_LOG, "r") as f:
        content = f.read()
    print(content if content else "No conflicts found.")
    log_event("rotor_conflict_report: Displayed all arbiter conflicts.")

if __name__ == "__main__":
    report_conflicts()
