# ~/Soap/rotor_core.py

import subprocess
import time
import os

def rotor_sync_cycle():
    while True:
        print("[+SPIN-UP+] ROTOR STATUS: 🌀 Starting Rotor Core Synchronization Loop")

        # Run fusion engine
        try:
            subprocess.run(["python3", "rotor_fusion.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"[Rotor Error] ❌ Rotor fusion failed: {e}")

        print("[+SPIN-UP+] ROTOR STATUS: ⏳ Sleeping 4 seconds before next cycle\n")
        time.sleep(4)

if __name__ == "__main__":
    rotor_sync_cycle()
