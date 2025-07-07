#!/usr/bin/env python3
"""
rotor_health_check.py: Verify the health of ATI Rotor Fusion and timing chain systems.

Checks:
  - Core rotor-related processes are running
  - Log files are fresh (updated within threshold)

Usage:
  python3 rotor_health_check.py
"""
import subprocess
import time
from pathlib import Path

# Configuration
HOME_DIR = Path.home()
LOG_DIR = HOME_DIR / "Soap" / "data" / "logs"
PROCESS_NAMES = [
    "attention.py", 
    "rotor_fusion.py", 
    "fusion_restore_v2.py", 
    "rotor_overlay.py", 
    "code_red.py",
    "spin_up.py",
    "spin_down.py"
]
# Map component to its log filename
LOG_COMPONENTS = {
    "Attention": "attention.log",
    "Fusion Restore": "restore.log",
    "Overlay Sync": "overlay.log",
    "Code-Red": "code_red.log",
    "Spin-Up": "spin_up.log",
    "Spin-Down": "spin_down.log"
}

FRESH_THRESHOLD = 120  # seconds

def check_processes():
    print("🔎 Checking rotor processes...")
    ps_output = subprocess.getoutput("ps aux")
    for proc in PROCESS_NAMES:
        count = sum(1 for line in ps_output.splitlines() if proc in line and 'grep' not in line)
        status = "RUNNING" if count > 0 else "NOT FOUND"
        print(f"  {proc}: {status}")


def check_logs():
    print("\n🔎 Checking log freshness...")
    now = time.time()
    for comp, log_file in LOG_COMPONENTS.items():
        path = LOG_DIR / log_file
        if not path.exists():
            print(f"  {comp}: LOG MISSING ({log_file})")
            continue
        age = now - path.stat().st_mtime
        if age <= FRESH_THRESHOLD:
            status = "OK"
        else:
            status = f"STALE ({int(age)}s)"
        print(f"  {comp}: {status}")


def main():
    print("=== ATI Rotor Health Check ===")
    check_processes()
    check_logs()
    print("\n✅ Health check complete.")

if __name__ == "__main__":
    main()
