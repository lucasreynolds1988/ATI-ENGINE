#!/usr/bin/env python3
import os, hashlib, json

BASE = os.path.expanduser('~/Soap')
OUTFILE = os.path.join(BASE, 'overlay', 'manifest.json')
manifest = {"protected": []}

def is_bloat(path):
    bloat_flags = [
        '/venv/', '__pycache__', '.log', '.cache', '.zip', '.part', '.gstmp', '.tmp',
        '/backups/', 'chunk_', 'relay_', 'rotor.log', '.ipynb_checkpoints', '.DS_Store'
    ]
    return any(flag in path for flag in bloat_flags)

def sha256sum(filepath):
    with open(filepath, 'rb') as f:
        h = hashlib.sha256()
        for chunk in iter(lambda: f.read(4096), b""): h.update(chunk)
        return h.hexdigest()

print("🔍 Scanning system for all protected files...\n")
for root, dirs, files in os.walk(BASE):
    for file in files:
        fpath = os.path.join(root, file)
        if not is_bloat(fpath) and os.path.isfile(fpath):
            try:
                manifest["protected"].append({
                    "path": fpath,
                    "sha256": sha256sum(fpath)
                })
            except Exception as e:
                print(f"⚠️ Skipped: {fpath} ({e})")

with open(OUTFILE, 'w') as f:
    json.dump(manifest, f, indent=2)

print(f"\n✅ Full manifest written to: {OUTFILE}")
print(f"🔐 {len(manifest['protected'])} protected files locked.")
