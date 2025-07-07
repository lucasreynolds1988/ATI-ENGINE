# ~/Soap/rotor_safety_check.py

import subprocess
import time
from pathlib import Path
from datetime import datetime

SHA_LOG = Path.home() / "Soap/data/sha_log.json"
RESTORE_LOG = Path.home() / "Soap/logs/rotor_safety_check.log"

def log(msg):
    with open(RESTORE_LOG, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

def main():
    log("🛡️ Safety check running.")
    if not SHA_LOG.exists():
        log("⚠️ SHA log missing. Triggering full restore...")
        print("⚠️ SHA log missing — running full restore...")
        subprocess.run(["python3", str(Path.home() / "Soap/fusion_restore_v2.py")])
    else:
        print("✅ SHA log present. No restore needed.")
        log("SHA log verified.")

    time.sleep(4)

if __name__ == "__main__":
    main()
