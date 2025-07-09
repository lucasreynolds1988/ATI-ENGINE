import os
import json
import zipfile
from core.rotor_overlay import log_event
from core.cloud_stream_relay import stream_to_cloud

BASE = os.path.expanduser("~/Soap")
MANIFEST_PATH = os.path.join(BASE, "overlay/manifest.json")
PROTECTED_DIRS = ["core", "agents", "overlay", "eyes"]
SAFE_EXT = [".py", ".json", ".log", ".zip"]
TRASH_EXT = [".tmp", ".gstmp", ".part"]

def load_manifest_paths():
    if not os.path.exists(MANIFEST_PATH):
        log_event("[SPIN-DOWN] ⚠️ No manifest found.")
        return []
    with open(MANIFEST_PATH, "r") as f:
        data = json.load(f)
        return [os.path.expanduser(entry["path"]) for entry in data]

def zip_safe_data(zip_path):
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, _, files in os.walk(BASE):
            if any(x in root for x in PROTECTED_DIRS):
                continue
            for file in files:
                fpath = os.path.join(root, file)
                arcname = os.path.relpath(fpath, BASE)
                zipf.write(fpath, arcname)

def purge_unneeded():
    protected = load_manifest_paths()
    for root, dirs, files in os.walk(BASE, topdown=False):
        for file in files:
            fpath = os.path.join(root, file)
            if any(p in fpath for p in protected) or any(x in fpath for x in PROTECTED_DIRS):
                log_event(f"[PROTECT] 🔒 {fpath}")
                continue
            if any(file.endswith(ext) for ext in TRASH_EXT) or file.startswith("."):
                try:
                    os.remove(fpath)
                    log_event(f"[TRASHED] 🗑️ {fpath}")
                except Exception as e:
                    log_event(f"[SKIP] ❌ {fpath}: {str(e)}")
        for d in dirs:
            dpath = os.path.join(root, d)
            if d in PROTECTED_DIRS or dpath in protected:
                continue
            try:
                os.rmdir(dpath)
                log_event(f"[DIR] ❌ Removed empty dir: {dpath}")
            except:
                pass

def main():
    log_event("[SPIN-DOWN] 🔻 Starting protected compression...")
    zip_path = os.path.join(BASE, "backups/ATI_SPINDOWN_BACKUP.zip")
    zip_safe_data(zip_path)
    stream_to_cloud(zip_path)
    purge_unneeded()
    log_event("[SPIN-DOWN] ✅ Completed safe purge.")

if __name__ == "__main__":
    main()
