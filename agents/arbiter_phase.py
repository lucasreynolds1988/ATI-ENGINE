# ~/Soap/agents/arbiter_phase.py

from core.rotor_overlay import log_event
from core.arbiter_knowledge import resolve_conflict

def detect_conflicts(sop_data):
    log_event("[ARBITER] 🧮 Running conflict detection scan...")

    conflict_sections = []
    if sop_data.get("technical_validation", {}).get("status") == "issues":
        conflict_sections.append("technical_validation")

    if "⚠️" in str(sop_data.get("safety", "")):
        conflict_sections.append("safety")

    if conflict_sections:
        sop_data["status"] = "draft"
        sop_data["conflict"] = resolve_conflict(
            "AR-101",
            f"Conflicts in sections: {', '.join(conflict_sections)}"
        )
    else:
        sop_data["status"] = "clean"

    return sop_data
