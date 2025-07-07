# ~/Soap/agents/arbiter_knowledge.py

def resolve_conflict(data):
    # Basic fallback resolution strategy
    watson = data.get("watson_backup", {})
    father = data.get("father_backup", {})
    mother = data.get("mother_backup", {})

    # If Father and Mother match, prefer their shared version
    fields = ["procedure", "tools", "materials", "safety"]
    resolved_fields = {}
    for field in fields:
        f = father.get(field)
        m = mother.get(field)
        if f == m and f is not None:
            resolved_fields[field] = f
        else:
            return "unresolved", f"Field conflict on '{field}'"

    # Merge resolved fields back into data
    for k, v in resolved_fields.items():
        data[k] = v

    return "resolved", "Father and Mother matched"
