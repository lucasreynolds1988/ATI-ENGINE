import os
import subprocess
from core.rotor_overlay import log_event

def unzip_overlay(zip_path):
    overlay = os.path.expanduser("~/Soap/overlay")
    subprocess.run(["unzip", "-o", zip_path, "-d", overlay])
    log_event(f"rotor_overlay_unzip: Extracted {zip_path} to overlay.")
    print(f"Extracted {zip_path} to overlay.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        unzip_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_unzip.py <zip_path>")
