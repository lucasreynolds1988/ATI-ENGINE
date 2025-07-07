import os
from core.rotor_overlay import log_event

def clear_overlay():
    overlay = os.path.expanduser("~/Soap/overlay")
    for f in os.listdir(overlay):
        path = os.path.join(overlay, f)
        if os.path.isfile(path):
            os.remove(path)
            log_event(f"rotor_overlay_clear: Removed {path}")
    log_event("rotor_overlay_clear: Overlay cleared.")

if __name__ == "__main__":
    clear_overlay()
