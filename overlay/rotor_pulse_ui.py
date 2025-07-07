# ~/Soap/rotor_pulse_ui.py

import time
import json
import psutil
from pathlib import Path

PULSE_FILE = Path.home() / "Soap/data/rotor_pulse.json"
ROTORS = ["rotor_github.py", "rotor_mongo.py", "rotor_gcs.py", "rotor_fusion.py"]

def get_status():
    status = {}
    for rotor in ROTORS:
        status[rotor] = any(
            rotor in " ".join(proc.info['cmdline']) 
            for proc in psutil.process_iter(['cmdline']) 
            if proc.info['cmdline']
        )
    return status

def main():
    while True:
        pulse = get_status()
        with open(PULSE_FILE, "w") as f:
            json.dump(pulse, f)
        time.sleep(4)

if __name__ == "__main__":
    main()
