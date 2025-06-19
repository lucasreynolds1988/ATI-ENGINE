# pip_offloader.py

import os
import shutil
import subprocess
from datetime import datetime

# CONFIGURABLE SETTINGS
THRESHOLD_MB = 80
MAX_DISK_MB = 5000
PUSH_WAIT_SECONDS = 3  # minimum wait before another push
TARGET_DIR = os.path.expanduser("~/Soap/pip-mirror")
GIT_REPO = "https://github.com/lucasr610/Soap.git"

LOG_FILE = os.path.expanduser("~/Soap/data/logs/ops_log.txt")

def log(msg):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} [OFFLOADER] {msg}\n")

def get_dir_size_mb(path):
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total += os.path.getsize(fp)
    return total / (1024 * 1024)

def run_git_push():
    try:
        subprocess.run(["git", "add", "."], cwd=TARGET_DIR, check=True)
        subprocess.run(["git", "commit", "-m", f"🧹 Auto-push at {datetime.now()}"], cwd=TARGET_DIR, check=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=TARGET_DIR, check=True)
        log("Pushed pip-mirror to GitHub.")
    except Exception as e:
        log(f"Git push failed: {e}")

def run_cleanup():
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            try:
                os.remove(os.path.join(root, file))
            except Exception as e:
                log(f"Failed to delete {file}: {e}")
    log("Local pip-mirror cleared.")

def main():
    if not os.path.exists(TARGET_DIR):
        log("pip-mirror not found, creating...")
        os.makedirs(TARGET_DIR)

    mirror_size = get_dir_size_mb(TARGET_DIR)
    total_shell_usage = get_dir_size_mb("/")

    log(f"Mirror Size: {mirror_size:.2f}MB | Disk Used: {total_shell_usage:.2f}MB")

    if mirror_size >= THRESHOLD_MB or total_shell_usage >= MAX_DISK_MB:
        log("Threshold exceeded. Triggering GitHub push and cleanup...")
        run_git_push()
        run_cleanup()
    else:
        log("Below threshold. No action needed.")

if __name__ == "__main__":
    main()
