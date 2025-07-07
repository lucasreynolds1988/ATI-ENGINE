import os
import subprocess
from core.rotor_overlay import log_event

def tar_overlay(dest_tar):
    overlay = os.path.expanduser("~/Soap/overlay")
    subprocess.run(["tar", "-czf", dest_tar, "."], cwd=overlay)
    log_event(f"rotor_overlay_tar: Created tarball {dest_tar} from overlay.")
    print(f"Created overlay tarball: {dest_tar}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        tar_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_tar.py <destination_tar>")
