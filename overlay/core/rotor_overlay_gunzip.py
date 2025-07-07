import os
import gzip
import shutil
from core.rotor_overlay import log_event

def gunzip_overlay(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    gz_path = os.path.join(overlay, filename)
    if not gz_path.endswith(".gz"):
        print("File must have .gz extension.")
        return
    out_path = gz_path[:-3]
    with gzip.open(gz_path, "rb") as f_in, open(out_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    log_event(f"rotor_overlay_gunzip: Decompressed {filename} to {out_path}")
    print(f"Decompressed {filename} to {out_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        gunzip_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_gunzip.py <filename.gz>")
