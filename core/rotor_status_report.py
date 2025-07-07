import os
from core.rotor_overlay import log_event

def report_status():
    overlay = os.path.expanduser("~/Soap/overlay")
    n_files = len(os.listdir(overlay))
    log_event(f"rotor_status_report: {n_files} files in overlay.")

if __name__ == "__main__":
    report_status()
