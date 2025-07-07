import os
from core.rotor_overlay import log_event

def check_permissions():
    base = os.path.expanduser("~/Soap")
    incorrect = []
    for root, dirs, files in os.walk(base):
        for f in files:
            path = os.path.join(root, f)
            perm = oct(os.stat(path).st_mode)[-3:]
            if perm not in ["600", "644"]:
                incorrect.append((path, perm))
    if incorrect:
        for path, perm in incorrect:
            log_event(f"rotor_check_permissions: Wrong perm {perm} for {path}")
    else:
        log_event("rotor_check_permissions: All file permissions correct.")

if __name__ == "__main__":
    check_permissions()
