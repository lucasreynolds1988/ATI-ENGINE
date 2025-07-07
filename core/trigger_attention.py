import subprocess
from core.rotor_overlay import log_event

def run_attention():
    log_event("trigger_attention: Activating Attention module.")
    subprocess.run(["python3", "/home/lucasreynolds1988/Soap/core/attention.py"])

if __name__ == "__main__":
    run_attention()
