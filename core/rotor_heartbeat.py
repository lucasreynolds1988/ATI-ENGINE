import time
from core.rotor_overlay import log_event

def heartbeat():
    while True:
        log_event("rotor_heartbeat: System alive.")
        time.sleep(4)

if __name__ == "__main__":
    heartbeat()
