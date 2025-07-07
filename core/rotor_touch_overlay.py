import os
from core.rotor_overlay import log_event

def touch_overlay_file(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    with open(path, "a"):
        os.utime(path, None)
    log_event(f"rotor_touch_overlay: Touched {filename}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        touch_overlay_file(sys.argv[1])
    else:
        print("Usage: python rotor_touch_overlay.py <filename>")
