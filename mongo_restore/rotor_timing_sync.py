#!/usr/bin/env python3
"""
rotor_timing_sync.py: Verifies all rotors pulse on a 4-second cycle.
"""
import time
import psutil
from pathlib import Path
from datetime import datetime

LOG_PATH = Path.home() / "Soap/logs/rotor_timing_sync.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
ROTORS = ["rotor_fusion.py", "fusion_restore_v2.py", "rotor_overlay.py", "code_red.py"]

def log(msg):
    with open(LOG_PATH, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

def is_running(script):
    for proc in psutil.process_iter(['cmdline']):
        if proc.info['cmdline'] and script in proc.info['cmdline'][0]:
            return True
    return False

def main():
    log("⏱️ Timing sync started.")
    while True:
        print("⏱️ [TIMING SYNC] Checking rotor statuses…")
        for r in ROTORS:
            state = "✅ RUNNING" if is_running(r) else "❌ OFFLINE"
            print(f"  • {r}: {state}")
            log(f"{r}: {state}")
        time.sleep(4)

if __name__ == "__main__":
    main()
