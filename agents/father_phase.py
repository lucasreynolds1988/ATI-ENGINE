# ~/Soap/agents/father_phase.py

from core.rotor_overlay import log_event

def verify_logic(sop_data):
    log_event("[FATHER] 🧠 Verifying technical logic...")

    errors = []

    tools = sop_data.get("tools", [])
    procedure = sop_data.get("procedure", {})

    flat_steps = []
    for section in procedure.values():
        flat_steps.extend(section if isinstance(section, list) else [])

    for tool in tools:
        if not any(tool.lower() in step.lower() for step in flat_steps):
            errors.append(f"Tool '{tool}' not mentioned in procedure.")

    if errors:
        sop_data["technical_validation"] = {"status": "issues", "details": errors}
    else:
        sop_data["technical_validation"] = {"status": "pass"}

    return sop_data
