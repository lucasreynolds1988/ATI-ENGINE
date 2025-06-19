# ~/Soap/rotor_v2.py

import time
import subprocess
from governor import get_rpm
from watchdog import disk_ok
from mongo_cleaner import purge_oldest_files

LOG_PATH = "/home/lucasreynolds1988/Soap/data/logs/alternating_upload_log.txt"

def log(msg):
    print(msg)
    with open(LOG_PATH, "a") as f:
        f.write(f"[rotor_v2] {msg}\n")

def run(cmd, label):
    try:
        subprocess.run(cmd, check=True)
        log(f"✅ {label}")
    except subprocess.CalledProcessError as e:
        log(f"❌ {label} failed: {e}")

def main():
    log("🧠 Rotor V2 initiated — spinning 6-stroke AI alternator...")
    while True:
        # Safety check
        if not disk_ok():
            log("🛑 Rotor paused — low disk space.")
            time.sleep(10)
            continue

        # Auto-clean MongoDB if needed
        purge_oldest_files()

        # Governor adjusts timing
        rpm = get_rpm()
        if not rpm:
            log("🛑 Governor halted rotor due to critical space.")
            time.sleep(10)
            continue

        # Stroke 1: Upload GitHub + Mongo (shared uploader)
        run(["python3", "alternating_uploader.py"], "🔵 Upload to GitHub / 🔴 MongoDB")
        time.sleep(rpm)

        # Stroke 2: Load missing module from Mongo (frontend test)
        run(["python3", "smart_loader.py", "load", "frontend"], "⚪ Load from MongoDB")
        time.sleep(rpm)

        # Stroke 3: Re-attempt upload cycle
        run(["python3", "alternating_uploader.py"], "🔴 Upload to MongoDB / GitHub")
        time.sleep(rpm)

        # Stroke 4: Offload from GitHub-confirmed
        run(["python3", "smart_offloader.py"], "⚫ Offload GitHub-confirmed")
        time.sleep(rpm)

        # Stroke 5: Compress+Dedup logic handled inside uploader/offloader
        # Stroke 6: Watchdog/Governor re-check is implicit

if __name__ == "__main__":
    main()
