from core.rotor_overlay import log_event

CONFLICT_LOG = "/home/lucasreynolds1988/Soap/logs/arbiter_conflicts.log"

def resolve_conflict(section, options):
    """
    Flags section as conflicted, logs it, and provides user/tech warning.
    """
    log_event(f"Arbiter: Conflict in section '{section}' - flagged for admin review.")
    with open(CONFLICT_LOG, "a") as f:
        f.write(f"{section} | Choices: {options}\n")
    result = {
        "section": section,
        "conflict": True,
        "choices": options,
        "note": (
            "⚠️ CONFLICT HERE: Needs admin review. "
            "Recommend contacting OEM, lead supervisor, or master tech before proceeding."
        ),
        "approved": False,
        "admin_resolution": None,
    }
    return result

def admin_approve(section, admin_name):
    """
    Marks section as approved and removes conflict note.
    """
    log_event(f"Admin '{admin_name}' approved section '{section}'.")
    # In production, you would update the data store to mark as approved
    return {
        "section": section,
        "conflict": False,
        "note": f"✅ Approved by Admin: {admin_name}",
        "approved": True,
        "admin_resolution": None,
    }

def admin_deny(section, correction, admin_name):
    """
    Admin provides a corrected version; overwrites previous content.
    """
    log_event(f"Admin '{admin_name}' corrected section '{section}'.")
    # In production, store admin correction and clear conflict
    return {
        "section": section,
        "conflict": False,
        "note": f"❗Corrected by Admin: {admin_name}",
        "approved": True,
        "admin_resolution": correction,
    }

def choose_source(preferred, backup=None):
    """
    Prefer Watson (format), fall back to Father (logic).
    """
    if preferred:
        return preferred
    elif backup:
        log_event("Arbiter: Using backup source.")
        return backup
    else:
        log_event("Arbiter: No valid source found.")
        return None
