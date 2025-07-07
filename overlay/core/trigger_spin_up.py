import subprocess
from core.rotor_overlay import log_event

def run_spin_up():
    log_event("trigger_spin_up: Activating Spin Up.")
    subprocess.run(["python3", "/home/lucasreynolds1988/Soap/core/spin_up.py"])

if __name__ == "__main__":
    run_spin_up()
