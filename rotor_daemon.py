# ~/Soap/rotor_daemon.py

import os
import time
import threading
import subprocess
import psutil

TRIGGER_WORD = "+CODE-RED+"
DISK_LIMIT_MB = 5000
ROTATE_THRESHOLD_MB = 80
CHECK_INTERVAL = 10  # seconds
LOG_FILE = os.path.expanduser('~/Soap/data/logs/rotor.log')


def get_used_disk_mb():
    result = os.popen("du -sm --exclude=/home/lost+found /home /root | awk '{sum += $1} END {print sum}'").read()
    try:
        return int(result.strip())
    except:
        return 0


def is_rotor_running():
    for proc in psutil.process_iter(['pid', 'cmdline']):
        if proc.info['cmdline'] and 'rotor_fusion.py' in " ".join(proc.info['cmdline']):
            return True
    return False


def launch_rotor_background():
    with open(LOG_FILE, 'a') as log:
        subprocess.Popen(
            ['python3', 'rotor_fusion.py'],
            cwd=os.path.expanduser('~/Soap'),
            stdout=log,
            stderr=log
        )
    print("🌀 Rotor launched in background... Logging to rotor.log")


def monitor_disk():
    while True:
        used_mb = get_used_disk_mb()
        if used_mb >= DISK_LIMIT_MB and not is_rotor_running():
            print(f"🧨 DISK ALERT: {used_mb}MB used. Triggering rotor.")
            launch_rotor_background()
        time.sleep(CHECK_INTERVAL)


def monitor_trigger():
    print("🕵️♂️ Watching for +CODE-RED+ activation...")
    while True:
        try:
            with open("rotor_trigger.txt", "r") as f:
                command = f.read().strip()
                if command == TRIGGER_WORD and not is_rotor_running():
                    print("🚨 +CODE-RED+ DETECTED. Rotor FUSION engaged.")
                    launch_rotor_background()
                    open("rotor_trigger.txt", "w").close()
        except FileNotFoundError:
            open("rotor_trigger.txt", "w").close()
        time.sleep(2)


def start_rotor_daemon():
    print("🔁 ROTOR DAEMON ENGAGED — Full Monitoring Online.")
    threading.Thread(target=monitor_disk, daemon=True).start()
    threading.Thread(target=monitor_trigger, daemon=True).start()
    while True:
        time.sleep(60)


if __name__ == "__main__":
    start_rotor_daemon()
