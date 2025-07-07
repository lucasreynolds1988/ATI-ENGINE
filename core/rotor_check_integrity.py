import os
import hashlib

def sha256sum(filename):
    h = hashlib.sha256()
    b = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()

def check_integrity(ref_dir):
    overlay = os.path.expanduser("~/Soap/overlay")
    for fname in os.listdir(overlay):
        overlay_file = os.path.join(overlay, fname)
        ref_file = os.path.join(ref_dir, fname)
        if os.path.isfile(overlay_file) and os.path.isfile(ref_file):
            sha_overlay = sha256sum(overlay_file)
            sha_ref = sha256sum(ref_file)
            status = "MATCH" if sha_overlay == sha_ref else "MISMATCH"
            print(f"{fname}: {status}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        check_integrity(sys.argv[1])
    else:
        print("Usage: python rotor_check_integrity.py <reference_dir>")
