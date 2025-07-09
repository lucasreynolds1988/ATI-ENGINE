# ~/Soap/agents/soap_phase.py

from core.rotor_overlay import log_event
from agents.watson_phase import structure_sop
from agents.father_phase import verify_logic
from agents.mother_phase import inject_safety
from agents.arbiter_phase import detect_conflicts

def synthesize_final_sop(raw_input):
    log_event("[SOAP] 🤖 Launching SOP synthesis pipeline...")

    structured = structure_sop(raw_input)
    checked = verify_logic(structured)
    safe = inject_safety(checked)
    final = detect_conflicts(safe)

    log_event("[SOAP] ✅ SOP complete.")
    return final
