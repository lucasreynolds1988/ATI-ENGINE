# ~/Soap/alternating_uploader.py

import os
import time
import shutil
import tarfile
import subprocess
import pymongo
from bson import ObjectId
from datetime import datetime
from pymongo import MongoClient
from gridfs import GridFS
from threading import Thread

CONFIG = {
    "rpm": 4.0,
    "voltage_mb": 45,
    "rpm_boost_mode": {
        "active": True,
        "target_rpm": 2.6,
        "voltage_mb": 30,
        "trigger_disk_limit_gb": 3.0
    },
    "mongo_uri": "mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev",
    "github_repo_path": os.path.expanduser("~/Soap"),
    "target_dirs": ["frontend", "backend", "vectorizer", "manuals"],
    "log_file": os.path.expanduser("~/Soap/data/logs/alternating_upload_log.txt")
}


def get_disk_usage_gb():
    total, used, free = shutil.disk_usage("/")
    return used / (1024 ** 3)


def compress_directory(dir_path):
    archive_name = f"/tmp/{os.path.basename(dir_path)}_{int(time.time())}.tar.gz"
    with tarfile.open(archive_name, "w:gz") as tar:
        tar.add(dir_path, arcname=os.path.basename(dir_path))
    return archive_name


def upload_to_github(file_path):
    try:
        dest = os.path.join(CONFIG["github_repo_path"], os.path.basename(file_path))
        shutil.copy(file_path, dest)
        subprocess.run(["git", "add", "."], cwd=CONFIG["github_repo_path"])
        subprocess.run(["git", "commit", "-m", f"Offload: {os.path.basename(file_path)}"], cwd=CONFIG["github_repo_path"])
        subprocess.run(["git", "push"], cwd=CONFIG["github_repo_path"])
        log_event(f"✅ GitHub upload: {file_path}")
    except Exception as e:
        log_event(f"❌ GitHub error: {str(e)}")


def upload_to_mongodb(file_path):
    try:
        client = MongoClient(CONFIG["mongo_uri"])
        db = client["sop_backup"]
        fs = GridFS(db)
        with open(file_path, "rb") as f:
            file_id = fs.put(f, filename=os.path.basename(file_path))
        log_event(f"✅ MongoDB upload: {file_path} (ID: {file_id})")
    except Exception as e:
        log_event(f"❌ MongoDB error: {str(e)}")


def log_event(msg):
    os.makedirs(os.path.dirname(CONFIG["log_file"]), exist_ok=True)
    with open(CONFIG["log_file"], "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(msg)


def alternating_upload_loop():
    index = 0
    dirs = CONFIG["target_dirs"]
    while True:
        disk_gb = get_disk_usage_gb()
        rpm = CONFIG["rpm"]
        voltage = CONFIG["voltage_mb"]

        if CONFIG["rpm_boost_mode"]["active"] and disk_gb > CONFIG["rpm_boost_mode"]["trigger_disk_limit_gb"]:
            rpm = CONFIG["rpm_boost_mode"]["target_rpm"]
            voltage = CONFIG["rpm_boost_mode"]["voltage_mb"]

        if index >= len(dirs):
            index = 0

        dir_path = os.path.join(CONFIG["github_repo_path"], dirs[index])
        index += 1

        if not os.path.exists(dir_path):
            continue

        archive = compress_directory(dir_path)
        size_mb = os.path.getsize(archive) / (1024 ** 2)

        try:
            if size_mb <= voltage:
                upload_to_github(archive)
                time.sleep(rpm)
                upload_to_mongodb(archive)
                time.sleep(rpm)
            else:
                upload_to_mongodb(archive)
                time.sleep(rpm)
                upload_to_github(archive)
                time.sleep(rpm)
        finally:
            os.remove(archive)


def start_alternating_uploader():
    Thread(target=alternating_upload_loop, daemon=True).start()
    log_event("🌀 Alternating uploader running...")


if __name__ == "__main__":
    start_alternating_uploader()
    while True:
        time.sleep(1)
