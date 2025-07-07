import os
import json
from core.rotor_overlay import log_event

def arbiter(input_path, output_path):
    """
    Detects any conflicts or flags from Father/Mother.
    Marks for admin if found, else passes.
    """
    with open(input_path) as f:
        sop = json.load(f)
    notes = []
    if sop.get("logic_notes"):
        notes.append("Logic Issue: " + "; ".join(sop["logic_notes"]))
    if sop.get("safety_flags"):
        notes.append("Safety Issue: " + "; ".join(sop["safety_flags"]))
    sop["arbiter_flags"] = notes
    sop["approved"] = not bool(notes)
    with open(output_path, "w") as f:
        json.dump(sop, f, indent=2)
    log_event(f"Arbiter: SOP {'FLAGGED' if notes else 'APPROVED'}: {output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        arbiter(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python arbiter_phase.py <input_sop.json> <output_sop.json>")
