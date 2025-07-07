import time
import sys
from core.rotor_overlay import log_event

def show_pulse():
    while True:
        sys.stdout.write('\r[rotor: pulse 💓] ')
        sys.stdout.flush()
        time.sleep(4)

if __name__ == "__main__":
    log_event("rotor_pulse_ui: Rotor pulse started.")
    show_pulse()
