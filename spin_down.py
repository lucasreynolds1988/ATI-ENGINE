# ~/Soap/spin_down.py

import os
import subprocess
import signal
import time
from datetime import datetime
from relay_log_hook import run_viewer
from pathlib import Path

TRIGGER_FILE = Path.home() / "Soap/rotor_trigger.txt"
STATUS_LOG = Path.home() / "Soap/data/logs/spin_down_status.txt"

def stop_rotor():
    print("\n🛑 +SPIN-DOWN+ INITIATED")
    print("🔍 Searching for rotor_core.py process...")

    try:
        output = subprocess.check_output(["pgrep", "-f", "rotor_core.py"]).decode().strip()
        pids = output.splitlines()

        if not pids:
            print("⚠️ No active rotor_core.py process found.")
            return

        for pid in pids:
            print(f"🧼 Terminating rotor_core.py (PID {pid})...")
            os.kill(int(pid), signal.SIGTERM)
            time.sleep(1)

        print("✅ Rotor core shut down successfully.")

    except subprocess.CalledProcessError:
        print("⚠️ No rotor_core.py process currently running.")
    except Exception as e:
        print(f"❌ Error stopping rotor: {e}")

def finalize_backup():
    print("💾 Finalizing logs and backup status...")
    try:
        subprocess.run(["python3", os.path.expanduser("~/Soap/rotor_fusion.py")], check=True)
        print("✅ Final fusion pass complete.")
    except Exception as e:
        print(f"❌ Fusion backup error: {e}")

def reset_trigger():
    try:
        TRIGGER_FILE.write_text("")
        print("🚫 Trigger cleared.")
    except Exception as e:
        print(f"⚠️ Could not reset trigger: {e}")

def write_status_stamp():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    STATUS_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(STATUS_LOG, "a") as log:
        log.write(f"[{now}] Spin-down complete. Rotor stopped and fusion finalized.\n")

def main():
    stop_rotor()
    finalize_backup()
    reset_trigger()
    write_status_stamp()
    print("📊 Reviewing relay log summary...")
    run_viewer("summary")
    print("🛡️ +SPIN-DOWN+ SEQUENCE COMPLETE")

if __name__ == "__main__":
    main()
