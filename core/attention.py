import os
from core.rotor_overlay import log_event

def create_trigger():
    path = os.path.expanduser("~/Soap/overlay/.trigger.rebuild")
    with open(path, "w") as f:
        f.write("SYSTEM WAKE-UP\n")
    log_event("[ATTENTION] 🚨 Trigger file created.")

def main():
    create_trigger()
    log_event("[ATTENTION] 🧠 Wake sequence executed.")

if __name__ == "__main__":
    main()
