import subprocess
from core.rotor_overlay import log_event

def kick_all():
    # Restarts all major rotors
    subprocess.Popen(["python3", "/home/lucasreynolds1988/Soap/core/rotor_fusion.py"])
    subprocess.Popen(["python3", "/home/lucasreynolds1988/Soap/core/rotor_heartbeat.py"])
    subprocess.Popen(["python3", "/home/lucasreynolds1988/Soap/core/rotor_timing_sync.py"])
    log_event("rotor_cron_kick: All rotors started.")

if __name__ == "__main__":
    kick_all()
