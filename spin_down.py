# ~/Soap/spin_down.py

import os
import subprocess
import signal
import time

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
    subprocess.run(["python3", os.path.expanduser("~/Soap/rotor_fusion.py")])
    print("✅ Final fusion pass complete.")

def main():
    stop_rotor()
    finalize_backup()
    print("🛡️ +SPIN-DOWN+ SEQUENCE COMPLETE")

if __name__ == "__main__":
    main()
