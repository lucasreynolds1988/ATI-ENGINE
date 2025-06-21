# ~/Soap/pulse_controller.py

import time
import subprocess
from itertools import cycle

# Cloud rotors
ROTORS = {
    "GITHUB": "python3 ~/Soap/git_rotor.py",
    "MONGO": "python3 ~/Soap/mongo_rotor.py",
    "GCS":   "python3 ~/Soap/gcs_rotor.py"
}

# Time between rotors (seconds)
PULSE_DELAY = 4

def main():
    print("🫀 Pulse Controller Online — Cycling Rotors")
    rotor_cycle = cycle(ROTORS.items())

    while True:
        label, cmd = next(rotor_cycle)
        print(f"\n🔄 {label} Rotor Pulse ➤ {cmd}")
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ {label} Rotor failed: {e}")
        time.sleep(PULSE_DELAY)

if __name__ == "__main__":
    main()
