#!/usr/bin/env python3
"""
code_red.py: Offload files from the Soap/upload directory to MongoDB, GitHub, or GCS, then delete them.
Run with:
  python3 code_red.py
"""

import logging
import subprocess
import sys
from pathlib import Path
from hashlib import sha256

# --- Configuration ---
SOAP_DIR = Path.home() / "Soap"
UPLOAD_DIR = SOAP_DIR / "upload"
LOG_DIR = SOAP_DIR / "logs"

# Size thresholds (MB)
MONGO_MAX = 13.0
GITHUB_MAX = 80.0
GCS_MAX = 200.0

# Scripts and directories
MONGO_SCRIPT = SOAP_DIR / "mongo_safe_upload_v2.py"
AI_CORE_DIR = SOAP_DIR / "ai_core"
LOG_FILE = LOG_DIR / "code_red.log"

# --- Setup ---
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console = logging.StreamHandler(sys.stdout)
console.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
logging.getLogger().addHandler(console)


# --- Utility Functions ---
def file_sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()[:8]

def file_size_mb(path: Path) -> float:
    return path.stat().st_size / (1024 * 1024)

# --- Offload Logic ---
def offload_file(path: Path):
    size = file_size_mb(path)
    sha = file_sha(path)
    logging.info(f"📦 Scanning: {path.name} | {size:.2f} MB | SHA: {sha}")

    try:
        if size <= MONGO_MAX and MONGO_SCRIPT.exists():
            logging.info("💾 Offloading to MongoDB...")
            subprocess.run([sys.executable, str(MONGO_SCRIPT), str(path)], check=True)

        elif size <= GITHUB_MAX:
            logging.info("⬆️ Offloading to GitHub...")
            AI_CORE_DIR.mkdir(parents=True, exist_ok=True)
            dest = AI_CORE_DIR / path.name
            path.replace(dest)

            subprocess.run(['git', '-C', str(SOAP_DIR), 'add', str(dest.relative_to(SOAP_DIR))], check=True)
            subprocess.run(['git', '-C', str(SOAP_DIR), 'commit', '-m', f"🔁 Auto-push {path.name}"], check=True)
            subprocess.run(['git', '-C', str(SOAP_DIR), 'push'], check=True)

        elif size <= GCS_MAX:
            logging.info("☁️ Offloading to GCS...")
            subprocess.run(['gsutil', 'cp', str(path), f"gs://ati-rotor-fusion/{path.name}"], check=True)

        else:
            logging.warning(f"⚠️ Skipped (too large): {path.name} ({size:.2f} MB)")
            return

        path.unlink()
        logging.info(f"🧹 Deleted local file: {path.name}")

    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Offload failed: {path.name} — {e}")
    except Exception as e:
        logging.error(f"❌ Error deleting file: {path.name} — {e}")

# --- Main ---
def main():
    logging.info("🛡️ Starting Code-Red offload scan...")
    for f in UPLOAD_DIR.iterdir():
        if f.is_file():
            offload_file(f)
    logging.info("✅ Code-Red scan complete.")

if __name__ == "__main__":
    main()
