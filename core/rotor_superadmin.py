import os
import sys
from core.rotor_overlay import log_event

def approve_conflict(section, admin_name="superadmin"):
    from core.arbiter_knowledge import admin_approve
    approval = admin_approve(section, admin_name)
    log_event(f"rotor_superadmin: {section} approved by {admin_name}.")
    print(f"{section}: {approval['note']}")

def correct_conflict(section, correction, admin_name="superadmin"):
    from core.arbiter_knowledge import admin_deny
    correction_result = admin_deny(section, correction, admin_name)
    log_event(f"rotor_superadmin: {section} corrected by {admin_name}.")
    print(f"{section}: {correction_result['note']}")

def show_conflicts():
    conflict_log = "/home/lucasreynolds1988/Soap/logs/arbiter_conflicts.log"
    if os.path.isfile(conflict_log):
        with open(conflict_log) as f:
            print(f.read())
    else:
        print("No conflicts found.")

if __name__ == "__main__":
    # Usage: python rotor_superadmin.py show|approve <section>|correct <section> <correction>
    if len(sys.argv) == 2 and sys.argv[1] == "show":
        show_conflicts()
    elif len(sys.argv) == 3 and sys.argv[1] == "approve":
        approve_conflict(sys.argv[2])
    elif len(sys.argv) >= 4 and sys.argv[1] == "correct":
        section = sys.argv[2]
        correction = " ".join(sys.argv[3:])
        correct_conflict(section, correction)
    else:
        print("Usage:")
        print("  python rotor_superadmin.py show")
        print("  python rotor_superadmin.py approve <section>")
        print("  python rotor_superadmin.py correct <section> <correction>")
