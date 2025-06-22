# ~/Soap/memory_logger.py

import psutil
import time
from datetime import datetime
from pathlib import Path
import json

LOG_PATH = Path.home() / "Soap/data/logs/memory_log.json"
INTERVAL = 10  # seconds
MAX_ENTRIES = 100

def get_memory_snapshot():
    mem = psutil.virtual_memory()
    return {
        "timestamp": datetime.now().isoformat(),
        "used_MB": mem.used // (1024 * 1024),
        "total_MB": mem.total // (1024 * 1024),
        "percent": mem.percent
    }

def log_memory():
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    log_data = []

    if LOG_PATH.exists():
        try:
            with open(LOG_PATH, "r") as f:
                log_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            log_data = []

    while True:
        snapshot = get_memory_snapshot()
        log_data.append(snapshot)

        if len(log_data) > MAX_ENTRIES:
            log_data = log_data[-MAX_ENTRIES:]

        try:
            with open(LOG_PATH, "w") as f:
                json.dump(log_data, f, indent=2)
        except Exception as e:
            print(f"❌ Failed to write memory log: {e}")

        print(f"🧠 RAM: {snapshot['used_MB']}MB used ({snapshot['percent']}%)")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    log_memory()
