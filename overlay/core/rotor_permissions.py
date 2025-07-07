import os
from core.rotor_overlay import log_event

def fix_permissions():
    base = os.path.expanduser("~/Soap")
    for root, dirs, files in os.walk(base):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o700)
        for f in files:
            os.chmod(os.path.join(root, f), 0o600)
    log_event("rotor_permissions: Permissions set to 700/600 on all files/dirs.")

if __name__ == "__main__":
    fix_permissions()
