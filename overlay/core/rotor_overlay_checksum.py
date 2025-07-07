import os
import hashlib
import json

def generate_checksum_manifest():
    overlay = os.path.expanduser("~/Soap/overlay")
    manifest = {}
    for fname in os.listdir(overlay):
        fpath = os.path.join(overlay, fname)
        if os.path.isfile(fpath):
            h = hashlib.sha256()
            with open(fpath, "rb") as f:
                while chunk := f.read(8192):
                    h.update(chunk)
            manifest[fname] = h.hexdigest()
    with open(os.path.expanduser("~/Soap/overlay_checksum.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    print("Generated overlay_checksum.json")

def compare_checksum_manifest(manifest_file):
    overlay = os.path.expanduser("~/Soap/overlay")
    with open(manifest_file) as f:
        manifest = json.load(f)
    for fname, refsha in manifest.items():
        fpath = os.path.join(overlay, fname)
        if os.path.isfile(fpath):
            h = hashlib.sha256()
            with open(fpath, "rb") as fobj:
                while chunk := fobj.read(8192):
                    h.update(chunk)
            sha = h.hexdigest()
            result = "MATCH" if sha == refsha else "MISMATCH"
            print(f"{fname}: {result}")
        else:
            print(f"{fname}: MISSING")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        generate_checksum_manifest()
    elif len(sys.argv) == 2:
        compare_checksum_manifest(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_checksum.py [manifest.json]")
