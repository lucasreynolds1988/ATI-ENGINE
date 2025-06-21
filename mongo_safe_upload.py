# ~/Soap/rotor_fusion.py

import os
import time
import subprocess
from pathlib import Path

GITHUB_REPO_DIR = Path("/home/lucasreynolds1988/Soap")
MONGO_UPLOADER = Path("~/Soap/mongo_safe_upload.py").expanduser()
GCS_BUCKET = "gs://ati-rotor-bucket/fusion-backup"
LOG_PATH = Path("~/Soap/data/logs/ops_log.txt").expanduser()

def log_event(message):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a") as log:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] {message}\n")
    print(message)

def is_inside_repo(file_path):
    try:
        file_path = Path(file_path).resolve()
        return GITHUB_REPO_DIR in file_path.parents
    except Exception:
        return False

def git_push(file_path):
    try:
        if not is_inside_repo(file_path):
            log_event(f"⚠️ Skipping GitHub push: {file_path} is outside the repo")
            return False

        rel_path = os.path.relpath(file_path, GITHUB_REPO_DIR)
        subprocess.run(["git", "-C", str(GITHUB_REPO_DIR), "add", rel_path], check=True)
        subprocess.run(["git", "-C", str(GITHUB_REPO_DIR), "commit", "-m", f"🧠 Fusion: {rel_path}"], check=True)
        subprocess.run(["git", "-C", str(GITHUB_REPO_DIR), "push", "origin", "main"], check=True)
        return True
    except Exception as e:
        log_event(f"❌ Git push failed for {file_path}: {e}")
        return False

def mongo_upload(file_path):
    try:
        log_event(f"🚚 Routing {file_path} → MONGO")
        subprocess.run(["python3", str(MONGO_UPLOADER), str(file_path)], check=True)
        return True
    except subprocess.CalledProcessError:
        log_event(f"❌ MongoDB upload failed for {file_path}")
        return False

def gcs_upload(file_path):
    try:
        log_event(f"⏪ Fallback to GCS: {file_path}")
        subprocess.run(["gsutil", "cp", str(file_path), GCS_BUCKET], check=True)
        return True
    except subprocess.CalledProcessError:
        log_event(f"❌ GCS upload failed: {file_path}")
        return False

def delete_file(file_path):
    try:
        Path(file_path).unlink()
        log_event(f"🧹 Deleted local: {file_path}")
    except Exception as e:
        log_event(f"❌ Failed to delete {file_path}: {e}")

def process_file(file_path):
    file_path = Path(file_path)
    if file_path.is_dir() or not file_path.exists():
        return

    if git_push(file_path):
        delete_file(file_path)
    elif mongo_upload(file_path):
        delete_file(file_path)
    elif gcs_upload(file_path):
        delete_file(file_path)

def scan_and_run():
    home_path = Path("/home/lucasreynolds1988")
    for dirpath, _, filenames in os.walk(home_path):
        for name in filenames:
            full_path = Path(dirpath) / name
            if ".git" in str(full_path): continue
            process_file(full_path)

def main():
    print("🧠 Rotor FUSION online — full-system sync mode")
    dev_zone = input("Enter dev zone (frontend / backend / both / skip): ").strip().upper()
    log_event(f"🧠 Running system diagnostics...")

    status_check = Path("/home/lucasreynolds1988/status_check.py")
    if status_check.exists():
        subprocess.run(["python3", str(status_check)])
    else:
        log_event("python3: can't open file '/home/lucasreynolds1988/status_check.py': [Errno 2] No such file or directory")

    log_event(f"🧰 System readiness check complete for: {dev_zone} zone")
    log_event(f"Logs written to {LOG_PATH.name}")

    scan_and_run()

if __name__ == "__main__":
    main()
