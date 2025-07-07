import os
from core.rotor_overlay import log_event

def clean_ext(ext):
    overlay = os.path.expanduser("~/Soap/overlay")
    for fname in os.listdir(overlay):
        if fname.endswith(ext):
            path = os.path.join(overlay, fname)
            os.remove(path)
            log_event(f"rotor_overlay_clean_ext: Removed {fname}")
    print(f"Removed all files with extension {ext} from overlay.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        clean_ext(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_clean_ext.py <extension>")
