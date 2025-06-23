#!/usr/bin/env python3
"""
Rotor Fusion Engine
Orchestrates restoring data from cloud sources (GitHub, MongoDB) and offloading local data to GitHub, GCS, and MongoDB.
Usage:
  python3 rotor_fusion.py [mode]
Modes:
  restore  - Pull latest code and data, then run fusion_restore_v2
  offload  - Run code_red to offload local files
  full     - Perform both restore and offload in sequence (default)
"""
import argparse
import logging
import subprocess
import sys
from pathlib import Path

# Paths
HOME_DIR = Path.home()
SOAP_DIR = HOME_DIR / 'Soap'
CODE_RED_SCRIPT = SOAP_DIR / 'code_red.py'
RESTORE_SCRIPT = SOAP_DIR / 'fusion_restore_v2.py'
REPO_URL = 'https://github.com/lucasr610/Soap.git'

def setup_logging():
    log_dir = SOAP_DIR / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / 'rotor_fusion.log'
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

def run_cmd(cmd, exit_on_fail=True):
    logging.info(f"⚙️ Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        logging.info(result.stdout.strip())
    if result.stderr:
        logging.error(result.stderr.strip())
    if exit_on_fail and result.returncode != 0:
        logging.error(f"Command failed (exit {result.returncode}), aborting.")
        sys.exit(result.returncode)

def sync_repo():
    git_dir = SOAP_DIR / '.git'
    if not git_dir.exists():
        logging.info(f"Cloning repo to {SOAP_DIR}")
        run_cmd(f"git clone {REPO_URL} {SOAP_DIR}")
    else:
        logging.info(f"Pulling latest changes in {SOAP_DIR}")
        run_cmd(f"git -C {SOAP_DIR} pull origin main", exit_on_fail=False)

def main():
    parser = argparse.ArgumentParser(description='Rotor Fusion Engine')
    parser.add_argument('mode', nargs='?', choices=['restore','offload','full'], default='full',
                        help='Mode to run: restore, offload, or full (default)')
    args = parser.parse_args()

    setup_logging()
    logging.info(f"Starting Rotor Fusion in '{args.mode}' mode")

    if args.mode in ('restore', 'full'):
        sync_repo()
        run_cmd(f"python3 {RESTORE_SCRIPT}")

    if args.mode in ('offload', 'full'):
        run_cmd(f"python3 {CODE_RED_SCRIPT}")

    logging.info("✅ Rotor Fusion complete.")

if __name__ == '__main__':
    main()
