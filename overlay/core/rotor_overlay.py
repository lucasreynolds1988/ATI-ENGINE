import os
import time

LOG_FILE = os.path.expanduser("~/Soap/logs/rotor_overlay.log")

def log_event(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")
