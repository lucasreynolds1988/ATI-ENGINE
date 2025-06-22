# ~/Soap/rotor_fusion.py

import time
import subprocess

def pulse_fusion_rotor():
    print("⚙️ [Rotor Fusion] Starting timed pulse loop...")
    while True:
        subprocess.call(["python3", "/home/lucasreynolds1988/Soap/fusion_restore_v2.py"])
        time.sleep(60)

if __name__ == "__main__":
    pulse_fusion_rotor()
