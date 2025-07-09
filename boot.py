# ~/Soap/boot.py

#!/usr/bin/env python3
import argparse, logging, subprocess, sys, os
from pathlib import Path
from hashlib import sha256

DEFAULT_ROOTS = [Path("/home"), Path("/root")]
EXCLUDE = [".git", "logs", "data", "core", "secrets", "overlay", "rotor_logs"]
DEFAULT_MONGO_MAX = 13
DEFAULT_GITHUB_MAX = 80
DEFAULT_GCS_MAX = 200
SOAP_DIR = Path.home() / "Soap"
GITHUB_SUBDIR = Path("ai_core")

def setup_logging():
    log_file = SOAP_DIR / "logs/code_red.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=str(log_file),
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

def file_sha(path): return sha256(path.read_bytes()).hexdigest()
def file_size_mb(path): return path.stat().st_size / (1024 * 1024)

def offload_file(path, mongo_max, github_max, gcs_max):
    size = file_size_mb(path)
    logging.info(f"📦 {path} | {size:.2f} MB | SHA {file_sha(path)[:8]}")
    try:
        if size <= mongo_max:
            subprocess.run([sys.executable, str(SOAP_DIR / "core/mongo_safe_upload_v2.py"), str(path)], check=True)
        elif size <= github_max:
            dest = SOAP_DIR / GITHUB_SUBDIR / path.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            path.replace(dest)
            subprocess.run(["git", "-C", str(SOAP_DIR), "add", str(dest.relative_to(SOAP_DIR))], check=True)
            subprocess.run(["git", "-C", str(SOAP_DIR), "commit", "-m", f"Auto-push {path.name}"], check=True)
            subprocess.run(["git", "-C", str(SOAP_DIR), "push"], check=True)
        elif size <= gcs_max:
            subprocess.run(["gsutil", "cp", str(path), f"gs://ati-rotor-fusion/{path.name}"], check=True)
        else:
            logging.warning(f"⚠️ Too large: {size:.2f} MB, skipping {path}")
            return
        path.unlink()
        logging.info(f"🧹 Deleted local file: {path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Offload failed for {path}: {e}")

def scan_and_offload(roots, mongo_max, github_max, gcs_max):
    for root in roots:
        for path in root.rglob('*'):
            if path.is_file() and not any(part in EXCLUDE for part in path.parts):
                offload_file(path, mongo_max, github_max, gcs_max)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--roots", nargs="+", type=Path, default=DEFAULT_ROOTS)
    parser.add_argument("--mongo-max", type=float, default=DEFAULT_MONGO_MAX)
    parser.add_argument("--github-max", type=float, default=DEFAULT_GITHUB_MAX)
    parser.add_argument("--gcs-max", type=float, default=DEFAULT_GCS_MAX)
    args = parser.parse_args()

    setup_logging()
    scan_and_offload(args.roots, args.mongo_max, args.github_max, args.gcs_max)
    logging.info("✅ Code-Red offload complete.")

if __name__ == "__main__":
    main()
