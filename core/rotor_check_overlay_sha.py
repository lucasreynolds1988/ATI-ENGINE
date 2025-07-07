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

def check_overlay_sha():
    overlay = os.path.expanduser("~/Soap/overlay")
    for fname in os.listdir(overlay):
        fpath = os.path.join(overlay, fname)
        if os.path.isfile(fpath):
            sha = sha256sum(fpath)
            print(f"{fname}: {sha}")

if __name__ == "__main__":
    check_overlay_sha()
