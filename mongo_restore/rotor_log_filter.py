# ~/Soap/rotor_log_filter.py

import time
from pathlib import Path
from datetime import datetime

LOG_DIR = Path.home() / "Soap/logs"
MAX_LOG_SIZE_MB = 5

def prune_logs():
    for log in LOG_DIR.glob("*.log"):
        if log.stat().st_size > MAX_LOG_SIZE_MB * 1024 * 1024:
            with open(log, "w") as f:
                f.write(f"[{datetime.now()}] 🔁 Log pruned due to size limit.\n")

def main():
    while True:
        prune_logs()
        time.sleep(8)

if __name__ == "__main__":
    main()
