# ~/Soap/agents/watson_phase.py

from core.rotor_overlay import log_event

def structure_sop(raw):
    log_event("[WATSON] 📐 Structuring raw input into SOP format...")

    return {
        "title": raw.get("title", "").strip(),
        "version": raw.get("version", "1.0"),
        "date": raw.get("date", ""),
        "status": raw.get("status", "draft"),
        "purpose": raw.get("purpose", "").strip(),
        "scope": raw.get("scope", "").strip(),
        "safety": raw.get("safety", "").strip(),
        "tools": raw.get("tools", []),
        "materials": raw.get("materials", []),
        "procedure": {
            "A": raw.get("procedure_A", []),
            "B": raw.get("procedure_B", []),
            "C": raw.get("procedure_C", []),
            "D": raw.get("procedure_D", []),
        },
        "troubleshooting": raw.get("troubleshooting", []),
        "maintenance": raw.get("maintenance", []),
        "references": raw.get("references", []),
        "definitions": raw.get("definitions", [])
    }
