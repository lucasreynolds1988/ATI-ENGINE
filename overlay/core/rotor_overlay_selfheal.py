import os
import subprocess
import json
import hashlib

def self_heal(manifest_file, backup_zip):
    overlay = os.path.expanduser("~/Soap/overlay")
    with open(manifest_file) as f:
        manifest = json.load(f)
    failed = False
    for fname, refsha in manifest.items():
        fpath = os.path.join(overlay, fname)
        if os.path.isfile(fpath):
            h = hashlib.sha256()
            with open(fpath, "rb") as fobj:
                while chunk := fobj.read(8192):
                    h.update(chunk)
            sha = h.hexdigest()
            if sha != refsha:
                print(f"{fname}: SHA256 FAIL")
                failed = True
        else:
            print(f"{fname}: MISSING")
            failed = True
    if failed:
        print("Checksum failed. Restoring overlay from backup.")
        subprocess.run(["unzip", "-o", backup_zip, "-d", overlay])
        print("Overlay restored.")
    else:
        print("Overlay integrity verified.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        self_heal(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python rotor_overlay_selfheal.py <checksum_manifest.json> <backup_zip>")
