import os
import shutil
import subprocess
import hashlib
import json
from pathlib import Path

GITHUB_REPO_DIR = "/home/lucasreynolds1988/Soap"
GCS_BUCKET = "gs://ati-rotor-bucket/fusion-backup"
FUSION_LOG = os.path.expanduser("~/Soap/.fusion-log.json")

# Track already pushed files (sha256)
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
        rel_path = os.path.relpath(file_path, GITHUB_REPO_DIR)
        subprocess.run(["git", "-C", GITHUB_REPO_DIR, "add", rel_path])
        subprocess.run(["git", "-C", GITHUB_REPO_DIR, "commit", "-m", f"🧠 Fusion: {rel_path}"])
        subprocess.run(["git", "-C", GITHUB_REPO_DIR, "push", "origin", "main"])
        return True
    except Exception as e:
        print(f"Git push failed for {file_path}: {e}")
        return False

def mongo_stub(file_path):
    print(f"[Mongo Stub] Marking {file_path.name} for MongoDB ingest")
    return True  # placeholder for real logic

def gcs_upload(file_path):
    try:
        subprocess.run(["gsutil", "cp", str(file_path), GCS_BUCKET], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"GCS upload failed: {file_path} — {e}")
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
    elif kind == "mongo":
        success = mongo_stub(file_path)
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

if __name__ == "__main__":
    print("🧠 Rotor FUSION online — full-system sync mode")
    scan_and_run()
