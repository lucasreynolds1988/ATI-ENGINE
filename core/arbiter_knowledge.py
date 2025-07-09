# ~/Soap/core/arbiter_knowledge.py

from core.rotor_overlay import log_event

def resolve_conflict(conflict_id, details):
    log_event(f"[ARBITER] ⚖️ Conflict {conflict_id} flagged.")
    log_event(f"[ARBITER] 🔍 Detail: {details}")
    return f"⚠️ CONFLICT {conflict_id} - REVIEW REQUIRED: {details}"
