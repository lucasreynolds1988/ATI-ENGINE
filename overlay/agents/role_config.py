# ~/Soap/agents/role_config.py

ROLES = [
    {"role": "Admin", "permissions": ["all"]},
    {"role": "Technician", "permissions": ["read", "run", "submit"]},
    {"role": "Curator", "permissions": ["read", "submit", "review"]},
    {"role": "Guest", "permissions": ["read"]}
]

def get_roles():
    return ROLES
