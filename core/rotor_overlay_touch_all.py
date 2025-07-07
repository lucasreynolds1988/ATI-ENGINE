import os
from core.rotor_overlay import log_event

def touch_all():
    overlay = os.path.expanduser("~/Soap/overlay")
    for fname in os.listdir(overlay):
        path = os.path.join(overlay, fname)
        if os.path.isfile(path):
            with open(path, "a"):
                os.utime(path, None)
            log_event(f"rotor_overlay_touch_all: Touched {fname}")
    print("Touched all overlay files.")

if __name__ == "__main__":
    touch_all()
