import time
from core.rotor_overlay import log_event

def rotor_timing():
    cycle = 0
    while True:
        cycle += 1
        log_event(f"rotor_timing_sync: Heartbeat {cycle}")
        time.sleep(4)

if __name__ == "__main__":
    rotor_timing()
