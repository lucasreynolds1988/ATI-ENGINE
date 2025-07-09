# ~/Soap/core/rotor_overlay.py

import os
from datetime import datetime

LOG_PATH = os.path.expanduser("~/Soap/overlay/rotor.log")

def log_event(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    entry = f"{timestamp} {message}"
    print(entry)
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(entry + "\n")
