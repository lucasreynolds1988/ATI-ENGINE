# ~/Soap/agents/trigger_spin_up.py

import sys
import os

def trigger():
    print("SPIN-UP: Initiating restore/startup sequence.", flush=True)
    # Create a trigger file for startup
    with open(os.path.expanduser("~/Soap/.startup_marker"), "w") as f:
        f.write("startup\n")
    print("Startup trigger file created.")

if __name__ == "__main__":
    trigger()
