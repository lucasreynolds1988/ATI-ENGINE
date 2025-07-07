import os
import shutil

def restore_overlay(src_dir):
    overlay = os.path.expanduser("~/Soap/overlay")
    os.makedirs(overlay, exist_ok=True)
    for fname in os.listdir(src_dir):
        src = os.path.join(src_dir, fname)
        dst = os.path.join(overlay, fname)
        if os.path.isfile(src):
            shutil.copy2(src, dst)
    print(f"Restored overlay from {src_dir}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        restore_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_restore.py <source_dir>")
