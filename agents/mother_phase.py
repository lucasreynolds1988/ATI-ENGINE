import os
import json
from core.rotor_overlay import log_event

def mother_check(sop_path, out_path):
    """
    Add safety/OSHA logic. Flags missing warnings, PPE, lockout/tagout.
    """
    with open(sop_path) as f:
        sop = json.load(f)
    safety_flags = []
    safety_section = sop.get("safety", [])
    if not any("PPE" in str(item).upper() for item in safety_section):
        safety_flags.append("No PPE listed in safety section.")
    if not any("lockout" in str(item).lower() for item in safety_section):
        safety_flags.append("No lockout/tagout statement.")
    sop["safety_flags"] = safety_flags
    with open(out_path, "w") as f:
        json.dump(sop, f, indent=2)
    log_event(f"Mother: Checked SOP, flags: {safety_flags}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        mother_check(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python mother_phase.py <input_sop.json> <output_sop.json>")
