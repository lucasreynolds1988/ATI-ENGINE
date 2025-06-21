# ~/Soap/auto_rebuilder.py

import os
import json
import subprocess
from pathlib import Path
import hashlib

FUSION_LOG = os.path.expanduser("~/Soap/.fusion-log.json")
RESTORE_DIR = os.path.expanduser("~/Soap_overlay")

def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def file_exists_and_valid(entry):
    path = Path(entry["path"])
    if not path.exists():
        return False
    try:
        return sha256(path) == list(log.keys())[list(log.values()).index(entry)]
    except:
        return False

def attempt_restore(filename):
    print(f"🛠️ Attempting restore: {filename}")
    try:
        subprocess.run(["python3", "fusion_restore_v2.py", filename], check=True)
    except subprocess.CalledProcessError:
        print(f"❌ Restore failed: {filename}")

def load_log():
    return json.load(open(FUSION_LOG)) if os.path.exists(FUSION_LOG) else {}

def main():
    global log
    log = load_log()
    print("🔍 Scanning SHA log for missing files...\n")

    for sha, entry in log.items():
        expected_path = Path(entry["path"])
        if not expected_path.exists():
            print(f"🚨 Missing: {expected_path}")
            attempt_restore(expected_path.name)
        else:
            print(f"✅ Present: {expected_path}")

    print("\n🧠 Rebuild check complete.")

if __name__ == "__main__":
    main()
