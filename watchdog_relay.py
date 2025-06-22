# ~/Soap/watchdog_relay.py

import os
import time
import subprocess
import psutil
from datetime import datetime
from pathlib import Path

WATCH_INTERVAL = 60  # seconds
ROTOR_NAME = "rotor_fusion.py"
RELAUNCH_CMD = ["python3", os.path.expanduser("~/Soap/rotor_fusion.py")]
LOG_FILE = Path.home() / "Soap/data/logs/watchdog_relay.log"

def is_rotor_running():
    for proc in psutil.process_iter(['pid', 'cmdline']):
        if proc.info['cmdline'] and ROTOR_NAME in " ".join(proc.info['cmdline']):
            return True
    return False

def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as log:
        log.write(f"[{timestamp}] {message}\n")
    print(f"🔍 {message}")

def restart_rotor():
    log_event("⚠️ Rotor not detected. Relaunching...")
    try:
        subprocess.Popen(RELAUNCH_CMD, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        log_event("✅ Rotor FUSION relaunched by watchdog.")
    except Exception as e:
        log_event(f"❌ Failed to restart rotor: {e}")

def watchdog_loop():
    log_event("🛡️ Watchdog Relay activated.")
    while True:
        if not is_rotor_running():
            restart_rotor()
        time.sleep(WATCH_INTERVAL)

if __name__ == "__main__":
    watchdog_loop()
