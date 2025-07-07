import os
from core.rotor_overlay import log_event

def clean_triggers():
    soap_root = os.path.expanduser("~/Soap")
    for f in os.listdir(soap_root):
        if f.startswith(".trigger"):
            os.remove(os.path.join(soap_root, f))
            log_event(f"rotor_trigger_cleaner: Removed {f}")

if __name__ == "__main__":
    clean_triggers()
