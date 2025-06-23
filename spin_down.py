#!/usr/bin/env python3
"""
spin_down.py: Gracefully sync and stop rotors.
"""
import subprocess
import time
from pathlib import Path

LOG_PATH = Path.home() / "Soap/logs/spin_down.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def log(msg):
    with open(LOG_PATH, "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

def main():
    print("🧹 [SPIN-DOWN] Saving state and offloading…")
    log("Spin-Down initiated.")
    try:
        subprocess.run(["python3", str(Path.home() / "Soap" / "code_red.py")], check=True)
        log("Code-Red offload complete.")
    except subprocess.CalledProcessError:
        log("Code-Red failed during Spin-Down.")
    print("💤 [SPIN-DOWN] All systems synced. Shutting down.")
    log("Spin-Down complete.")

if __name__ == "__main__":
    main()
