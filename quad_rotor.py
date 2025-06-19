# ~/Soap/quad_rotor.py

import time
import subprocess
from datetime import datetime

LOG_PATH = "/home/lucasreynolds1988/Soap/data/logs/alternating_upload_log.txt"

def log_event(message):
    with open(LOG_PATH, "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")
    print(message)

def run(script_command, label):
    try:
        subprocess.run(script_command, check=True)
        log_event(f"✅ {label}")
    except subprocess.CalledProcessError as e:
        log_event(f"❌ {label} failed: {e}")

def main():
    log_event("🌀 quad_rotor.py engaged — 4-Pole Alternator now live...")
    while True:
        run(["python3", "alternating_uploader.py"], "🔵 Upload to GitHub / 🔴 MongoDB")
        time.sleep(2)
        run(["python3", "smart_loader.py", "load", "frontend"], "⚪ Load from MongoDB")
        time.sleep(2)
        run(["python3", "alternating_uploader.py"], "🔴 Upload to MongoDB / 🔵 GitHub")
        time.sleep(2)
        run(["python3", "smart_offloader.py"], "⚫ Offload GitHub-confirmed modules")
        time.sleep(2)

if __name__ == "__main__":
    main()
