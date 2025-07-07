import os
import json
from core.rotor_overlay import log_event

def father_check(sop_path, out_path):
    """
    Add logic/tech validation. Returns SOP with logic notes.
    """
    with open(sop_path) as f:
        sop = json.load(f)
    notes = []
    # Check for required fields, sample logic
    if not sop.get("procedure"):
        notes.append("No procedure steps found.")
    if not sop.get("materials"):
        notes.append("No materials listed.")
    sop["logic_notes"] = notes
    with open(out_path, "w") as f:
        json.dump(sop, f, indent=2)
    log_event(f"Father: Checked SOP, notes: {notes}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        father_check(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python father_phase.py <input_sop.json> <output_sop.json>")
