# ~/Soap/watchdog_diskspace.py
import os
import shutil
import time
from pathlib import Path

# === SETTINGS ===
THRESHOLD_MB = 500  # Trigger cleanup if free space < 500MB
CHECK_INTERVAL_SEC = 300  # Check every 5 minutes

def get_free_space_mb():
    stat = shutil.disk_usage("/home")
    return stat.free // (1024 * 1024)

def clean_temp():
    deleted = 0
    targets = list(Path("/tmp").glob("*.tar.gz")) + list(Path("/home/lucasreynolds1988/Soap").glob("*.tar.gz"))
    for file in targets:
        try:
            file.unlink()
            print(f"🧹 Deleted: {file}")
            deleted += 1
        except Exception as e:
            print(f"❌ Failed to delete {file}: {e}")
    return deleted

def clean_cache():
    for path in ["~/.npm", "~/.cache", "~/Soap/__pycache__"]:
        full = os.path.expanduser(path)
        if os.path.exists(full):
            shutil.rmtree(full, ignore_errors=True)
            print(f"🧹 Purged: {full}")

def watchdog_loop():
    while True:
        free_mb = get_free_space_mb()
        print(f"🧭 Disk check: {free_mb}MB free")

        if free_mb < THRESHOLD_MB:
            print("🚨 Low disk space! Initiating cleanup...")
            count = clean_temp()
            clean_cache()
            print(f"✅ Cleanup done. {count} files removed.")
        else:
            print("✅ Disk space sufficient. No cleanup needed.")

        time.sleep(CHECK_INTERVAL_SEC)

if __name__ == "__main__":
    watchdog_loop()
