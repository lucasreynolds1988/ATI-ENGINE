import os
from core.rotor_overlay import log_event

def wake_up_sequence():
    marker = os.path.expanduser("~/Soap/.trigger.rebuild")
    with open(marker, "w") as f:
        f.write("rebuild\n")
    log_event("Attention: System wake-up marker created.")
    log_event("Attention: System ready for code_red and spin_up.")

if __name__ == "__main__":
    wake_up_sequence()
