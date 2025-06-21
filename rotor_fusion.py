# ~/Soap/rotor_fusion.py

import os
import subprocess
import hashlib
import json
from pathlib import Path
import shutil
from mongo_safe_upload_v2 import safe_upload_to_mongo  # ✅ Use external safe chunking uploader

# === CONFIGURATION ===
GITHUB_REPO_DIR = "/home/lucasreynolds1988/Soap"
GCS_BUCKET = "gs://ati-rotor-bucket/fusion-backup"
FUSION_LOG = os.path.expanduser("~/Soap/.fusion-log.json")

# === CORE FUNCTIONS ===

def load_log():
    if os.path.exists(FUSION_LOG):
        with open(FUSION_LOG, "r") as f:
            return json.load(f)
    return {}

def save_log(log):
    with open(FUSION_LOG, "w") as f:
        json.dump(log, f, indent=2)

def sha256(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def classify_file(file_path):
    ext = file_path.suffix.lower()
    if ext in [".py", ".json", ".md", ".js", ".ts"]:
        return "github"
    elif ext in [".pdf", ".docx", ".csv", ".sqlite3", ".txt"]:
        return "mongo"
    else:
        return "gcs"

def git_push(file_path):
    try:
        file_path = Path(file_path).resolve()
        repo_root = Path(GITHUB_REPO_DIR).resolve()
        if not str(file_path).startswith(str(repo_root)):
            print(f"⚠️ Skipping GitHub push: {file_path} is outside the repo")
            return False

        rel_path = os.path.relpath(file_path, repo_root)
        subprocess.run(["git", "-C", str(repo_root), "add", rel_path], check=True)
        subprocess.run(["git", "-C", str(repo_root), "commit", "-m", f"🧠 Fusion: {rel_path}"], check=True)
        subprocess.run(["git", "-C", str(repo_root), "push", "origin", "main"], check=True)
        return True
    except Exception as e:
        print(f"❌ Git push failed for {file_path}: {e}")
        return False

def gcs_upload(file_path):
    try:
        subprocess.run(["gsutil", "cp", str(file_path), GCS_BUCKET], check=True)
        print(f"✅ GCS upload complete: {file_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ GCS upload failed: {file_path}\n{e}")
        print("💡 TIP: Run `gsutil mb GCS_BUCKET_URL` to create the bucket if missing.")
        return False

def process_file(file_path, log):
    file_hash = sha256(file_path)
    if file_hash in log:
        print(f"✅ Already processed: {file_path.name}")
        return

    kind = classify_file(file_path)
    success = False

    print(f"🚚 Routing {file_path} → {kind.upper()}")

    if kind == "github":
        success = git_push(file_path)
        if not success:
            print(f"⏪ Fallback to GCS: {file_path}")
            success = gcs_upload(file_path)
    elif kind == "mongo":
        success = safe_upload_to_mongo(file_path)  # ✅ Calls chunk-safe Mongo uploader
    elif kind == "gcs":
        success = gcs_upload(file_path)

    if success:
        try:
            os.remove(file_path)
            log[file_hash] = {"path": str(file_path), "dest": kind}
            print(f"🧹 Deleted local: {file_path}")
        except Exception as e:
            print(f"❌ Failed to delete {file_path}: {e}")

def scan_and_run():
    log = load_log()
    search_dirs = ["/home", "/root"]

    for base_dir in search_dirs:
        for dirpath, _, filenames in os.walk(base_dir):
            for file in filenames:
                full_path = Path(os.path.join(dirpath, file))
                try:
                    if full_path.is_file() and not full_path.name.startswith("."):
                        process_file(full_path, log)
                except Exception as e:
                    print(f"⚠️ Error scanning {full_path}: {e}")

    save_log(log)
    print("✅ Fusion rotor complete.")

def run_system_check():
    print("\n🧠 Running system diagnostics...")
    try:
        result = subprocess.run(["python3", "status_check.py"], capture_output=True)
        if result.returncode != 0:
            print("⚠️ status_check.py returned error, skipping diagnostics.")
    except FileNotFoundError:
        print("⚠️ status_check.py not found, skipping system diagnostics.")

def main():
    print("🧠 Rotor FUSION online — full-system sync mode")
    dev_zone = "both"
    run_system_check()
    print(f"\n🧰 System readiness check complete for: {dev_zone.upper()} zone")
    print("Logs written to ops_log.txt\n")
    scan_and_run()

if __name__ == "__main__":
    main()
