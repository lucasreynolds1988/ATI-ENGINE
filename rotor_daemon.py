# ~/Soap/rotor_daemon.py

import os
import time
import threading
import subprocess

TRIGGER_WORD = "+CODE-RED+"
DISK_LIMIT_MB = 5000
ROTATE_THRESHOLD_MB = 80
CHECK_INTERVAL = 10  # seconds

def get_used_disk_mb():
    result = os.popen("du -sm /home /root | awk '{sum += $1} END {print sum}'").read()
    try:
        return int(result.strip())
    except:
        return 0

def monitor_disk():
    while True:
        used_mb = get_used_disk_mb()
        if used_mb >= DISK_LIMIT_MB:
            print(f"🧨 DISK ALERT: {used_mb}MB used. Triggering rotor.")
            run_rotor()
        time.sleep(CHECK_INTERVAL)

def monitor_trigger():
    print("🕵️‍♂️ Watching for +CODE-RED+ activation...")
    while True:
        try:
            with open("rotor_trigger.txt", "r") as f:
                command = f.read().strip()
                if command == TRIGGER_WORD:
                    print("🚨 +CODE-RED+ DETECTED. Rotor FUSION engaged.")
                    run_rotor()
                    open("rotor_trigger.txt", "w").close()  # Reset trigger
        except FileNotFoundError:
            open("rotor_trigger.txt", "w").close()  # Create trigger file
        time.sleep(2)

def run_rotor():
    subprocess.run(["python3", "fusion_rotor.py"])

if __name__ == "__main__":
    print("🔁 ROTOR DAEMON ENGAGED — Monitoring System Online.")
    threading.Thread(target=monitor_disk, daemon=True).start()
    threading.Thread(target=monitor_trigger, daemon=True).start()
    while True:
        time.sleep(60)
