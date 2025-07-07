import os
from core.rotor_overlay import log_event

def clean_logs():
    logs_dir = os.path.expanduser("~/Soap/logs")
    for f in os.listdir(logs_dir):
        if f.endswith(".log"):
            os.remove(os.path.join(logs_dir, f))
            log_event(f"rotor_logs_cleaner: Removed {f}")

if __name__ == "__main__":
    clean_logs()
