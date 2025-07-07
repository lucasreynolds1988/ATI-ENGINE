import os
import subprocess
import time
from core.rotor_overlay import log_event

def run_script(path):
    subprocess.run(["python3", path], check=True)

def full_boot():
    log_event("+BOOT+: System startup initiated.")
    open("/home/lucasreynolds1988/Soap/.trigger.rebuild", "w").close()
    run_script("core/attention.py")     # wakeup system
    run_script("core/code_red.py")      # offload old upload queue
    run_script("core/spin_up.py")       # restore backup and relaunch rotor
    log_event("+BOOT+: System is now online.")

if __name__ == "__main__":
    full_boot()
