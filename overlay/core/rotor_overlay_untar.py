import os
import subprocess
from core.rotor_overlay import log_event

def untar_overlay(tar_path):
    overlay = os.path.expanduser("~/Soap/overlay")
    subprocess.run(["tar", "-xzf", tar_path, "-C", overlay])
    log_event(f"rotor_overlay_untar: Extracted {tar_path} to overlay.")
    print(f"Extracted {tar_path} to overlay.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        untar_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_untar.py <tar_path>")
