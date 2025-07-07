import subprocess
from core.rotor_overlay import log_event

def run_all():
    procs = [
        subprocess.Popen(["python3", "/home/lucasreynolds1988/Soap/core/rotor_fusion.py"]),
        subprocess.Popen(["python3", "/home/lucasreynolds1988/Soap/core/rotor_heartbeat.py"]),
        subprocess.Popen(["python3", "/home/lucasreynolds1988/Soap/core/rotor_timing_sync.py"]),
        subprocess.Popen(["python3", "/home/lucasreynolds1988/Soap/core/rotor_pulse_ui.py"])
    ]
    log_event("rotor_run_all: All core rotors started.")
    for p in procs:
        p.wait()

if __name__ == "__main__":
    run_all()
