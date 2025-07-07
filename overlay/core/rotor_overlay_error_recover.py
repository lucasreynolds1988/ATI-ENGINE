import os
import subprocess

def error_recover(backup_zip):
    overlay = os.path.expanduser("~/Soap/overlay")
    if not os.listdir(overlay):
        print("Overlay is empty or corrupted. Attempting recovery...")
        subprocess.run(["unzip", "-o", backup_zip, "-d", overlay])
        print("Recovery attempt complete.")
    else:
        print("Overlay is not empty. No recovery needed.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        error_recover(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_error_recover.py <backup_zip>")
