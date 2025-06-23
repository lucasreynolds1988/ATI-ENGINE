# ~/Soap/cloud_stream_relay.py

import time
import hashlib
from pathlib import Path
from rotor_overlay import log_event

STREAM_DIR = Path.home() / "Soap/data/stream"
LOG_PATH = Path.home() / "Soap/logs/stream_relay.log"
GCS_BUCKET = "ati-rotor-fusion"
DELAY_INTERVAL = 4  # seconds between pulses

def sha256sum(path):
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha.update(block)
    return sha.hexdigest()

def relay_stream():
    log_event("🔄 [RELAY] Cloud Stream Relay starting...", LOG_PATH)
    if not STREAM_DIR.exists():
        STREAM_DIR.mkdir(parents=True)

    while True:
        for file in STREAM_DIR.glob("**/*"):
            if file.is_file():
                sha = sha256sum(file)
                log_event(f"🌐 Streaming {file.name} [SHA: {sha}]", LOG_PATH)
                # Simulate offload (replace with GCS push later)
                file.unlink()  # Emulate memory release
        log_event("⏱️ Pulse cycle complete. Sleeping...", LOG_PATH)
        time.sleep(DELAY_INTERVAL)

if __name__ == "__main__":
    relay_stream()
