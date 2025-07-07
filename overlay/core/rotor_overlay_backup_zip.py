import os
import subprocess
from core.rotor_overlay import log_event

def backup_zip(dest_zip):
    overlay = os.path.expanduser("~/Soap/overlay")
    subprocess.run(["zip", "-r", dest_zip, "."], cwd=overlay)
    log_event(f"rotor_overlay_backup_zip: Created backup zip {dest_zip} from overlay")
    print(f"Backup zip created: {dest_zip}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        backup_zip(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_backup_zip.py <destination_zip>")
