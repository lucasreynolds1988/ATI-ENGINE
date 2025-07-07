import os
import shutil

def cross_backup(dest_dir):
    overlay = os.path.expanduser("~/Soap/overlay")
    os.makedirs(dest_dir, exist_ok=True)
    for fname in os.listdir(overlay):
        src = os.path.join(overlay, fname)
        dst = os.path.join(dest_dir, fname)
        if os.path.isfile(src):
            shutil.copy2(src, dst)
            print(f"Copied {fname} to {dest_dir}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        cross_backup(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_cross_backup.py <external_dir>")
