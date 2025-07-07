import os
import json
from core.rotor_overlay import log_event

def soap_finalize(input_path, output_path):
    """
    Final pass: explain/teach to tech. Summarizes warnings, logic, safety, references.
    """
    with open(input_path) as f:
        sop = json.load(f)
    summary = ["--- SOP FINAL OUTPUT FOR TECHNICIAN ---"]
    summary.append(f"Title: {sop.get('title','')}")
    if sop.get("arbiter_flags"):
        summary.append("**ADMIN REVIEW REQUIRED**")
        summary.extend(sop["arbiter_flags"])
    else:
        summary.append("APPROVED FOR USE")
    summary.append("Procedure:")
    for step in sop.get("procedure", []):
        summary.append(f"- {step}")
    summary.append("Safety:")
    for flag in sop.get("safety_flags", []):
        summary.append(f"! {flag}")
    with open(output_path, "w") as f:
        f.write("\n".join(summary))
    log_event(f"Soap: Final SOP explanation written to {output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        soap_finalize(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python soap_phase.py <input_sop.json> <output.txt>")
