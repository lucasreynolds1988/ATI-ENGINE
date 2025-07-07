import os
import shutil

def restore_parts(prefix, src_dir):
    overlay = os.path.expanduser("~/Soap/overlay")
    files = [f for f in os.listdir(src_dir) if f.startswith(prefix) and ".part" in f]
    for f in files:
        src = os.path.join(src_dir, f)
        dst = os.path.join(overlay, f)
        shutil.copy2(src, dst)
        print(f"Restored {f} to overlay")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        restore_parts(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python rotor_overlay_restore_parts.py <prefix> <src_dir>")
