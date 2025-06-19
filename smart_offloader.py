# ~/Soap/smart_offloader.py

import os
import time
import shutil
import tarfile
import hashlib
import subprocess
import pymongo
from bson import ObjectId
from datetime import datetime
from pymongo import MongoClient
from gridfs import GridFS

CONFIG = {
    "rpm": 4.0,
    "voltage_mb": 45,
    "mongo_uri": "mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev",
    "github_repo_path": os.path.expanduser("~/Soap"),
    "target_dirs": ["frontend", "backend", "vectorizer", "manuals"],
    "log_file": os.path.expanduser("~/Soap/data/logs/alternating_upload_log.txt")
}


def log_event(msg):
    os.makedirs(os.path.dirname(CONFIG["log_file"]), exist_ok=True)
    with open(CONFIG["log_file"], "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(msg)


def get_file_hash(file_path):
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def already_exists_in_mongo(hash_value):
    client = MongoClient(CONFIG["mongo_uri"])
    db = client["sop_backup"]
    fs = GridFS(db)
    return fs.find_one({"metadata.hash": hash_value}) is not None


def already_exists_in_git(file_name):
    repo_path = CONFIG["github_repo_path"]
    full_path = os.path.join(repo_path, file_name)
    return os.path.exists(full_path)


def compress_and_hash(dir_path):
    archive = f"/tmp/{os.path.basename(dir_path)}_{int(time.time())}.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        tar.add(dir_path, arcname=os.path.basename(dir_path))
    file_hash = get_file_hash(archive)
    return archive, file_hash


def push_to_git(file_path):
    try:
        dest = os.path.join(CONFIG["github_repo_path"], os.path.basename(file_path))
        shutil.copy(file_path, dest)
        subprocess.run(["git", "add", "."], cwd=CONFIG["github_repo_path"])
        subprocess.run(["git", "commit", "-m", f"Offload mirror: {os.path.basename(file_path)}"], cwd=CONFIG["github_repo_path"])
        subprocess.run(["git", "push"], cwd=CONFIG["github_repo_path"])
        log_event(f"✅ GitHub mirror: {file_path}")
    except Exception as e:
        log_event(f"❌ GitHub push error: {e}")


def push_to_mongo(file_path, hash_value):
    try:
        client = MongoClient(CONFIG["mongo_uri"])
        db = client["sop_backup"]
        fs = GridFS(db)
        with open(file_path, "rb") as f:
            fs.put(f, filename=os.path.basename(file_path), metadata={"hash": hash_value})
        log_event(f"✅ MongoDB mirror: {file_path}")
    except Exception as e:
        log_event(f"❌ Mongo push error: {e}")


def offload_local_module(path):
    shutil.rmtree(path)
    log_event(f"🧹 Local module offloaded: {path}")


def execute_offloader():
    for module in CONFIG["target_dirs"]:
        local_path = os.path.join(CONFIG["github_repo_path"], module)
        if not os.path.exists(local_path):
            continue

        archive, file_hash = compress_and_hash(local_path)
        file_name = os.path.basename(archive)

        in_git = already_exists_in_git(file_name)
        in_mongo = already_exists_in_mongo(file_hash)

        if not in_git:
            push_to_git(archive)
            time.sleep(CONFIG["rpm"])
        if not in_mongo:
            push_to_mongo(archive, file_hash)
            time.sleep(CONFIG["rpm"])

        if in_git and in_mongo:
            offload_local_module(local_path)

        os.remove(archive)


if __name__ == "__main__":
    execute_offloader()
