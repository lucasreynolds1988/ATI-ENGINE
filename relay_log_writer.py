# ~/Soap/relay_log_writer.py

import json
from datetime import datetime
from pathlib import Path

LOG_PATH = Path.home() / "Soap/logs/relay_log.json"

def append_log(sha, cloud, size=0, chunk_id=None, **kwargs):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if LOG_PATH.exists():
        with open(LOG_PATH, "r") as f:
            entries = json.load(f)
    else:
        entries = []

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "sha": sha,
        "cloud": cloud,
        "size": size,
        "chunk_id": chunk_id or "?",
    }
    entry.update(kwargs)
    entries.append(entry)

    with open(LOG_PATH, "w") as f:
        json.dump(entries, f, indent=2)

    print(f"📝 Logged {sha[:8]} to {cloud}")
