import os
import shutil
from core.rotor_overlay import log_event

def restore_single(filename, src_dir):
    overlay = os.path.expanduser("~/Soap/overlay")
    src = os.path.join(src_dir, filename)
    dst = os.path.join(overlay, filename)
    if os.path.isfile(src):
        shutil.copy2(src, dst)
        log_event(f"rotor_overlay_restore_single: Restored {filename} from {src_dir}")
        print(f"Restored {filename} from {src_dir}")
    else:
        print(f"File {filename} not found in {src_dir}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        restore_single(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python rotor_overlay_restore_single.py <filename> <source_dir>")
