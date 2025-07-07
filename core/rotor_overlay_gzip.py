import os
import gzip
import shutil
from core.rotor_overlay import log_event

def gzip_overlay(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    gz_path = path + ".gz"
    with open(path, "rb") as f_in, gzip.open(gz_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    log_event(f"rotor_overlay_gzip: Compressed {filename} to {gz_path}")
    print(f"Compressed {filename} to {gz_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        gzip_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_gzip.py <filename>")
