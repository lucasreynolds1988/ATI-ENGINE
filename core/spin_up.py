import os
import json
import shutil
from core.fusion_restore_v2 import restore_from_manifest
from core.rotor_overlay import log_event

BASE = os.path.expanduser("~/Soap")
MANIFEST_PATH = os.path.join(BASE, "overlay/manifest.json")
PROTECTED_DIRS = ["core", "agents", "overlay", "eyes", "rotors", "wraps", "triggers"]
SKIP_EXT = [".tmp", ".gstmp", ".part", ".pyc", ".DS_Store", ".zip"]

def load_manifest_paths():
    if not os.path.exists(MANIFEST_PATH):
        return []
    with open(MANIFEST_PATH, "r") as f:
        return [os.path.expanduser(entry["path"]) for entry in json.load(f)]

def purge_bloat():
    protected = load_manifest_paths()
    log_event("[SPIN-UP] 🧹 Purging temp files...")
    for root, dirs, files in os.walk(BASE, topdown=False):
        for file in files:
            full_path = os.path.join(root, file)
            if full_path in protected or any(p in full_path for p in PROTECTED_DIRS):
                continue
            if any(full_path.endswith(ext) for ext in SKIP_EXT):
                try:
                    os.remove(full_path)
                    log_event(f"[PURGE] 🗑️ {full_path}")
                except: pass
        for d in dirs:
            if d in PROTECTED_DIRS:
                continue
            try:
                if not os.listdir(os.path.join(root, d)):
                    shutil.rmtree(os.path.join(root, d))
            except: pass

def load_manifest_data():
    try:
        with open(MANIFEST_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        log_event(f"[SPIN-UP] ❌ Manifest load failed: {str(e)}")
        return []

def restore_files():
    protected = load_manifest_paths()
    for entry in load_manifest_data():
        path = os.path.expanduser(entry["path"])
        if path in protected or any(p in path for p in PROTECTED_DIRS):
            log_event(f"[SPIN-UP] 🔒 Skipping protected file: {path}")
            continue
        restore_from_manifest(entry)

def rebuild_trigger():
    trigger = os.path.join(BASE, "overlay/.trigger.rebuild")
    if not os.path.exists(trigger):
        with open(trigger, "w") as f:
            f.write("TRIGGER")
        log_event("[SPIN-UP] 🧪 Rebuild trigger created.")

def main():
    log_event("[SPIN-UP] 🚀 Starting safe restore...")
    purge_bloat()
    rebuild_trigger()
    restore_files()
    purge_bloat()
    log_event("[SPIN-UP] ✅ Restore complete.")

if __name__ == "__main__":
    main()
