# ~/Soap/agents/trigger_spin_down.py

import sys
import os

def trigger():
    print("SPIN-DOWN: Initiating safe shutdown sequence.", flush=True)
    # Create a trigger file for shutdown
    with open(os.path.expanduser("~/Soap/.shutdown_marker"), "w") as f:
        f.write("shutdown\n")
    print("Shutdown trigger file created.")

if __name__ == "__main__":
    trigger()
