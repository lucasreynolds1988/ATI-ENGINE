import subprocess
import time
from core.rotor_overlay import log_event

def test_cycle():
    log_event("rotor_test_cycle: Starting test rotor cycle...")
    subprocess.run(["python3", "/home/lucasreynolds1988/Soap/core/rotor_fusion.py"])
    time.sleep(10)
    log_event("rotor_test_cycle: Completed one rotor cycle.")

if __name__ == "__main__":
    test_cycle()
