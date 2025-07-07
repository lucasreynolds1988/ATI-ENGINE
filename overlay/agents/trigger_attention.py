# ~/Soap/agents/trigger_attention.py

import sys
import os

def trigger():
    print("ATTENTION: System wake-up initiated.", flush=True)
    # Create a trigger file for downstream scripts
    with open(os.path.expanduser("~/Soap/.rebuild_marker"), "w") as f:
        f.write("wake\n")
    print("Trigger file created.")

if __name__ == "__main__":
    trigger()
