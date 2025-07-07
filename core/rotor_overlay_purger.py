import os
from core.rotor_overlay import log_event

def purge_overlay():
    overlay = os.path.expanduser("~/Soap/overlay")
    for fname in os.listdir(overlay):
        fpath = os.path.join(overlay, fname)
        if os.path.isfile(fpath):
            os.remove(fpath)
            log_event(f"rotor_overlay_purger: Removed {fname}")

if __name__ == "__main__":
    purge_overlay()
