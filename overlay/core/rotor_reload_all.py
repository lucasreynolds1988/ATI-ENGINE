import subprocess
from core.rotor_overlay import log_event

def reload_rotors():
    log_event("rotor_reload_all: Reloading all rotor services.")
    subprocess.Popen(["python3", "/home/lucasreynolds1988/Soap/core/rotor_fusion.py"])
    subprocess.Popen(["python3", "/home/lucasreynolds1988/Soap/core/rotor_timing_sync.py"])
    subprocess.Popen(["python3", "/home/lucasreynolds1988/Soap/core/rotor_safety_check.py"])
    subprocess.Popen(["python3", "/home/lucasreynolds1988/Soap/core/rotor_pulse_ui.py"])

if __name__ == "__main__":
    reload_rotors()
