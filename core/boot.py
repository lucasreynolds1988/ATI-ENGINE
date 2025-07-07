import os
import subprocess
import time
import sys

# Add parent directory to Python path so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.rotor_overlay import log_event

def run_script(path):
    try:
        subprocess.run(["python3", os.path.join("core", path)], check=True)
    except subprocess.CalledProcessError as e:
        log_event(f"+BOOT+: Error running {path} - {e}")

def full_boot():
    log_event("+BOOT+: System startup initiated.")
    open("/home/lucasreynolds1988/Soap/.trigger.rebuild", "w").close()
    run_script("attention.py")     # wakeup system
    run_script("code_red.py")      # offload old upload queue
    run_script("spin_up.py")       # restore backup and relaunch rotor
    log_event("+BOOT+: System is now online.")

if __name__ == "__main__":
    full_boot()
