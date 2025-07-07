#!/usr/bin/env python3
"""
code_red.py: Smart offload rotor for ATI SOP system.
Scans local directories, offloads files to appropriate backends (MongoDB, GitHub, GCS), and cleans up.
Usage:
  python3 code_red.py [--roots DIR [DIR ...]] [--mongo-max MB] [--github-max MB] [--gcs-max MB]
"""
import argparse
import logging
import subprocess
import sys
import os
from pathlib import Path
from hashlib import sha256

# Default configuration
DEFAULT_ROOTS = [Path("/home"), Path("/root")]
EXCLUDE = [".git", "logs", "data"]
DEFAULT_MONGO_MAX = 13    # MB
DEFAULT_GITHUB_MAX = 80   # MB
DEFAULT_GCS_MAX = 200     # MB
GITHUB_SUBDIR = Path('ai_core')  # relative to SOAP_DIR for GitHub offload
SOAP_DIR = Path.home() / 'Soap'


def setup_logging():
    log_dir = SOAP_DIR / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / 'code_red.log'
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


def file_sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def file_size_mb(path: Path) -> float:
    return path.stat().st_size / (1024 * 1024)


def offload_file(path: Path, mongo_max: float, github_max: float, gcs_max: float):
    size = file_size_mb(path)
    sha = file_sha(path)[:8]
    logging.info(f"📦 {path} | {size:.2f} MB | SHA {sha}")

    try:
        if size <= mongo_max:
            logging.info("💾 Offloading to MongoDB")
            subprocess.run(
                [sys.executable, str(SOAP_DIR / 'mongo_safe_upload_v2.py'), str(path)],
                check=True
            )
        elif size <= github_max:
            logging.info("⬆️ Offloading to GitHub")
            dest_dir = SOAP_DIR / GITHUB_SUBDIR
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_dir / path.name
            path.replace(dest)
            subprocess.run(
                ["git", "-C", str(SOAP_DIR), "add", str(dest.relative_to(SOAP_DIR))],
                check=True
            )
            subprocess.run(
                ["git", "-C", str(SOAP_DIR), "commit", "-m", f"🔁 Auto-push {path.name}"],
                check=True
            )
            subprocess.run(
                ["git", "-C", str(SOAP_DIR), "push"],
                check=True
            )
        elif size <= gcs_max:
            logging.info("☁️ Offloading to GCS")
            subprocess.run(
                ["gsutil", "cp", str(path), f"gs://ati-rotor-fusion/{path.name}"],
                check=True
            )
        else:
            logging.warning(f"⚠️ File too large for offload: {size:.2f} MB, skipping: {path}")
            return
    except subprocess.CalledProcessError as e:
        logging.error(f"Offload failed for {path}: {e}")
        return

    # Remove local file after successful offload
    try:
        path.unlink()
        logging.info(f"🧹 Deleted local file: {path}")
    except Exception as e:
        logging.error(f"Failed to delete {path}: {e}")


def scan_and_offload(roots, mongo_max, github_max, gcs_max):
    logging.info("🛡️ Starting Code-Red offload scan...")
    for root in roots:
        for path in root.rglob('*'):
            if not path.is_file():
                continue
            if any(part in EXCLUDE for part in path.parts):
                continue
            offload_file(path, mongo_max, github_max, gcs_max)


def main():
    parser = argparse.ArgumentParser(description='Code-Red Offload Rotor')
    parser.add_argument('--roots', nargs='+', type=Path, default=DEFAULT_ROOTS,
                        help='Directories to scan')
    parser.add_argument('--mongo-max', type=float, default=DEFAULT_MONGO_MAX,
                        help='Max MB for MongoDB offload')
    parser.add_argument('--github-max', type=float, default=DEFAULT_GITHUB_MAX,
                        help='Max MB for GitHub offload')
    parser.add_argument('--gcs-max', type=float, default=DEFAULT_GCS_MAX,
                        help='Max MB for GCS offload')
    args = parser.parse_args()

    setup_logging()
    scan_and_offload(args.roots, args.mongo_max, args.github_max, args.gcs_max)
    logging.info("✅ Code-Red offload complete.")

if __name__ == '__main__':
    main()
