# ~/Soap/code_red.py

import os, time, subprocess
from pathlib import Path
from hashlib import sha256

ROOT_PATHS = [Path("/home"), Path("/root")]
EXCLUDE_DIRS = ["Soap/.git", "Soap/logs"]
MAX_GITHUB_MB, MAX_MONGO_MB, MAX_GCS_MB = 80, 13, 200

def get_sha(path):
    with open(path, "rb") as f: return sha256(f.read()).hexdigest()

def get_mb(path): return os.path.getsize(path) / (1024 * 1024)

def safe_push(path):
    size, sha = get_mb(path), get_sha(path)
    print(f"📦 {path.name} | {round(size, 2)}MB | SHA: {sha[:8]}")
    if size <= MAX_MONGO_MB:
        print("💽 Uploading to MongoDB...")
        subprocess.run(["python3", "mongo_safe_upload_v2.py", str(path)])
    elif size <= MAX_GITHUB_MB:
        print("⬆️ GitHub Push...")
        dest = Path("ai_core") / path.name
        os.system(f"cp {path} {dest}")
        subprocess.run(["git", "-C", str(Path.home() / "Soap"), "add", str(dest)])
        subprocess.run(["git", "-C", str(Path.home() / "Soap"), "commit", "-m", f"🔁 Auto-push: {path.name}"])
        subprocess.run(["git", "-C", str(Path.home() / "Soap"), "push"])
    elif size <= MAX_GCS_MB:
        print("☁️ GCS Upload...")
        subprocess.run(["gsutil", "cp", str(path), f"gs://ati-rotor-fusion/{path.name}"])
    print("🧹 Deleting...")
    os.remove(path)

def scan_all():
    print("🧨 [+CODE-RED+] FULL SYSTEM CHECK...")
    for root in ROOT_PATHS:
        for dirpath, _, files in os.walk(root):
            for f in files:
                path = Path(dirpath) / f
                if any(ex in str(path) for ex in EXCLUDE_DIRS): continue
                try:
                    if path.is_file(): safe_push(path); time.sleep(1)
                except Exception as e:
                    print(f"❌ {f}: {e}")

if __name__ == "__main__":
    scan_all()
