#!/usr/bin/env python3
"""
code_red.py: Offload files from the Soap/upload directory to MongoDB, GitHub, or GCS and then delete them.
Usage:
  python3 code_red.py
  or in background via cron/nohup
"""
import logging
import subprocess
import sys
from pathlib import Path
from hashlib import sha256

# Base paths
SOAP_DIR = Path.home() / 'Soap'
UPLOAD_DIR = SOAP_DIR / 'upload'
LOG_DIR = SOAP_DIR / 'logs'

# Offload thresholds (in MB)
MONGO_MAX = 13.0
GITHUB_MAX = 80.0
GCS_MAX = 200.0

# Paths to helper scripts
MONGO_SCRIPT = SOAP_DIR / 'mongo_safe_upload_v2.py'

# Ensure directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Setup logging
def setup_logging():
    log_file = LOG_DIR / 'code_red.log'
    logging.basicConfig(
        filename=str(log_file),
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
    logging.getLogger().addHandler(console)

# Compute SHA-256
def file_sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()[:8]

# Size in MB
def file_size_mb(path: Path) -> float:
    return path.stat().st_size / (1024 * 1024)

# Offload a single file
def offload_file(path: Path):
    size = file_size_mb(path)
    sha = file_sha(path)
    logging.info(f"📦 {path.name} | {size:.2f} MB | SHA {sha}")
    try:
        if size <= MONGO_MAX and MONGO_SCRIPT.exists():
            logging.info("💾 Offloading to MongoDB...")
            subprocess.run([sys.executable, str(MONGO_SCRIPT), str(path)], check=True)
        elif size <= GITHUB_MAX:
            logging.info("⬆️ Offloading to GitHub...")
            dest_dir = SOAP_DIR / 'ai_core'
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_dir / path.name
            path.replace(dest)
            for cmd in [
                ['git','-C',str(SOAP_DIR),'add',str(dest.relative_to(SOAP_DIR))],
                ['git','-C',str(SOAP_DIR),'commit','-m',f"🔁 Auto-push {path.name}"],
                ['git','-C',str(SOAP_DIR),'push']
            ]:
                subprocess.run(cmd, check=True)
        elif size <= GCS_MAX:
            logging.info("☁️ Offloading to GCS...")
            subprocess.run(['gsutil','cp',str(path),f"gs://ati-rotor-fusion/{path.name}"], check=True)
        else:
            logging.warning(f"⚠️ Skipping too-large file: {path.name} ({size:.2f} MB)")
            return
    except subprocess.CalledProcessError as e:
        logging.error(f"Offload failed for {path.name}: {e}")
        return
    # Cleanup
    try:
        path.unlink()
        logging.info(f"🧹 Deleted local file: {path.name}")
    except Exception as e:
        logging.error(f"Failed to delete {path.name}: {e}")

# Scan upload directory
def main():
    setup_logging()
    logging.info("🛡️ Starting Code-Red offload scan of upload directory...")
    for file in UPLOAD_DIR.iterdir():
        if file.is_file():
            offload_file(file)
    logging.info("✅ Code-Red offload complete.")

if __name__ == '__main__':
    main()
