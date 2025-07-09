# ~/Soap/agents/mother_phase.py

from core.rotor_overlay import log_event

def inject_safety(sop_data):
    log_event("[MOTHER] 🧯 Enforcing OSHA-compliant safety formatting...")

    safety = sop_data.get("safety", "")
    if not all(x in safety for x in ["WHAT", "WHY", "CORRECTION"]):
        structured_safety = "\n".join([
            "WHAT: Identify the potential hazard involved.",
            "WHY: Explain the risk to technician or equipment.",
            "CORRECTION: Describe how to mitigate or prevent the hazard."
        ])
        sop_data["safety"] = f"{safety.strip()}\n\n{structured_safety}".strip()

    sop_data["safety_validation"] = {"status": "enforced"}

    return sop_data
