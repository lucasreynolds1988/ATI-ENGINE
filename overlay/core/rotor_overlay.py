import time
from pathlib import Path

LOG_FILE = Path.home() / "Soap/rotor_logs/rotor_overlay.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def log_event(event, level="INFO"):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} [{level}] {event}\n")
    print(f"[{level}] {event}")

if __name__ == "__main__":
    log_event("rotor_overlay test log entry", "DEBUG")
