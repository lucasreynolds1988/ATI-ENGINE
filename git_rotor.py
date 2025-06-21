# ~/Soap/git_rotor.py

import os
import subprocess
import hashlib
import json
from pathlib import Path

REPO_DIR = os.path.expanduser("~/Soap")
LOG_PATH = os.path.expanduser("~/Soap/.fusion-log.json")

def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def load_log():
    return json.load(open(LOG_PATH)) if os.path.exists(LOG_PATH) else {}

def save_log(log):
    with open(LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)

def git_push(file_path, rel_path):
    try:
        subprocess.run(["git", "-C", REPO_DIR, "add", rel_path], check=True)
        subprocess.run(["git", "-C", REPO_DIR, "commit", "-m", f"🔁 Auto-push: {rel_path}"], check=True)
        subprocess.run(["git", "-C", REPO_DIR, "push", "origin", "main"], check=True)
        print(f"✅ Git pushed: {rel_path}")
        return True
    except Exception as e:
        print(f"❌ Git push failed for {rel_path}: {e}")
        return False

def scan_and_push():
    log = load_log()
    for dirpath, _, filenames in os.walk(REPO_DIR):
        for filename in filenames:
            full_path = Path(os.path.join(dirpath, filename))
            try:
                if not full_path.is_file(): continue
                if full_path.name.startswith("."): continue

                file_hash = sha256(full_path)
                if log.get(file_hash): continue

                rel_path = os.path.relpath(full_path, REPO_DIR)
                if git_push(full_path, rel_path):
                    log[file_hash] = {
                        "path": str(full_path),
                        "dest": "github"
                    }
            except Exception as e:
                print(f"⚠️ Error on {full_path}: {e}")
    save_log(log)

if __name__ == "__main__":
    scan_and_push()
