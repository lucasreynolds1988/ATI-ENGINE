# ~/Soap/rotor_github.py

import subprocess
import time
from pathlib import Path
from datetime import datetime

UPLOAD_PATH = Path.home() / "Soap/upload"
LOG_PATH = Path.home() / "Soap/logs/rotor_github.log"

LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def log(msg):
    with open(LOG_PATH, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] {msg}\n")

def push_to_git():
    try:
        subprocess.run(["git", "-C", str(Path.home() / "Soap"), "add", "."], check=True)
        subprocess.run(["git", "-C", str(Path.home() / "Soap"), "commit", "-m", "🔁 Auto-push: rotor upload"], check=True)
        subprocess.run(["git", "-C", str(Path.home() / "Soap"), "push"], check=True)
        log("✅ GitHub push complete.")
    except subprocess.CalledProcessError:
        log("⚠️ GitHub push skipped or failed.")

def main():
    while True:
        push_to_git()
        time.sleep(8)  # avoid hammering

if __name__ == "__main__":
    main()
