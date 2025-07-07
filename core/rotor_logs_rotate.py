import os
import shutil
import time
from core.rotor_overlay import log_event

def rotate_logs():
    logs_dir = os.path.expanduser("~/Soap/logs")
    archive_dir = os.path.join(logs_dir, "archive")
    os.makedirs(archive_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    for f in os.listdir(logs_dir):
        if f.endswith(".log"):
            src = os.path.join(logs_dir, f)
            dst = os.path.join(archive_dir, f"{f}.{timestamp}")
            shutil.move(src, dst)
            log_event(f"rotor_logs_rotate: Rotated {f} to archive.")

if __name__ == "__main__":
    rotate_logs()
