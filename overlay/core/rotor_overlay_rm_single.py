import os
from core.rotor_overlay import log_event

def rm_single(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if os.path.isfile(path):
        os.remove(path)
        log_event(f"rotor_overlay_rm_single: Removed {filename}")
        print(f"Removed {filename}")
    else:
        print(f"File {filename} not found in overlay.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        rm_single(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_rm_single.py <filename>")
