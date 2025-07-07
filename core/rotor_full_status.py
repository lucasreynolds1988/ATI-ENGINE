import os
import shutil
from core.rotor_overlay import log_event

def full_status():
    root = os.path.expanduser("~/Soap")
    overlay = os.path.join(root, "overlay")
    logs = os.path.join(root, "logs")
    disk = shutil.disk_usage(root)
    n_overlay = len(os.listdir(overlay))
    n_logs = len(os.listdir(logs))
    msg = (
        f"Overlay: {n_overlay} files | "
        f"Logs: {n_logs} files | "
        f"Disk Used: {disk.used//1024//1024}MB"
    )
    print(msg)
    log_event(f"rotor_full_status: {msg}")

if __name__ == "__main__":
    full_status()
