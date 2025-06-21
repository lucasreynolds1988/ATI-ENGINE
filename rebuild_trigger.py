# ~/Soap/rebuild_trigger.py

import os
import subprocess
from pathlib import Path

TRIGGER_FILE = Path.home() / ".trigger.rebuild"
NEEDED_FILES = [
    "~/Soap/spin_up.py",
    "~/Soap/rotor_core.py",
    "~/Soap/rotor_fusion.py",
    "~/Soap/fusion_loader.py",
]

GITHUB_REPO = "https://github.com/lucasr610/Soap.git"
LOCAL_SOAP_DIR = Path.home() / "Soap"

def check_trigger():
    if TRIGGER_FILE.exists():
        print("🟨 Trigger file detected: Rebuild required.")
        return True
    else:
        print("✅ No rebuild needed. System looks healthy.")
        return False

def create_trigger():
    TRIGGER_FILE.touch()
    print("🧷 Trigger file created. Use +REBUILD+ to restore.")

def delete_trigger():
    if TRIGGER_FILE.exists():
        TRIGGER_FILE.unlink()
        print("🗑️ Trigger file removed after successful rebuild.")

def file_missing(path_str):
    return not Path(os.path.expanduser(path_str)).exists()

def restore_from_github():
    print("📡 Pulling clean system from GitHub...")
    if LOCAL_SOAP_DIR.exists():
        subprocess.run(["git", "-C", str(LOCAL_SOAP_DIR), "pull"], check=True)
    else:
        subprocess.run(["git", "clone", GITHUB_REPO, str(LOCAL_SOAP_DIR)], check=True)

def run_rebuild():
    print("🧠 INITIATING +REBUILD+ SEQUENCE")
    restore_from_github()

    missing_after = [f for f in NEEDED_FILES if file_missing(f)]
    if not missing_after:
        print("✅ All system files restored.")
        delete_trigger()
    else:
        print("⚠️ Some files still missing:")
        for f in missing_after:
            print(f" - {f}")
        print("🧱 Rebuild incomplete — verify source availability.")

if __name__ == "__main__":
    if check_trigger():
        run_rebuild()
