def resolve_conflict(section_a, section_b):
    if section_a == section_b:
        return section_a
    return f"⚠️ CONFLICT HERE:\n-- Option A --\n{section_a}\n-- Option B --\n{section_b}"

def apply_arbiter_to_sections(sections):
    resolved = {}
    for key, val in sections.items():
        if isinstance(val, list) and len(val) == 2:
            resolved[key] = resolve_conflict(val[0], val[1])
        else:
            resolved[key] = val
    return resolved
