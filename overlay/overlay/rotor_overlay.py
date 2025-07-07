#!/usr/bin/env python3
import time
import logging
import os

HOME_DIR = os.path.expanduser("~")
LOGS_DIR = os.path.join(HOME_DIR, "Soap", "logs")
os.makedirs(LOGS_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOGS_DIR, "rotor_overlay.log")

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def log_event(event):
    logging.info(event)
    print(f"🧭 [OVERLAY] {event}")

def main():
    print("🧭 Rotor Overlay ONLINE. Logging heartbeat every 4 seconds.")
    while True:
        log_event("💓 Rotor Overlay heartbeat: system alive and rotating.")
        time.sleep(4)

if __name__ == "__main__":
    main()

