import subprocess
from core.rotor_overlay import log_event

def run_code_red():
    log_event("trigger_code_red: Activating Code Red.")
    subprocess.run(["python3", "/home/lucasreynolds1988/Soap/core/code_red.py"])

if __name__ == "__main__":
    run_code_red()
