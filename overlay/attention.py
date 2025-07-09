# ~/Soap/overlay/attention.py

import os
from core.rotor_overlay import log_event

def trigger_attention():
    log_event("📡 ATTENTION: Trigger signal received.")
    os.system("python3 ~/Soap/overlay/code_red.py")
    os.system("python3 ~/Soap/overlay/spin_up.py")

if __name__ == "__main__":
    trigger_attention()
