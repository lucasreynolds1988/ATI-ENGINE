import os
import shutil
from core.rotor_overlay import log_event

def report_disk():
    root = os.path.expanduser("~/Soap")
    total, used, free = shutil.disk_usage(root)
    msg = f"Disk usage for {root} - Total: {total//1024//1024}MB, Used: {used//1024//1024}MB, Free: {free//1024//1024}MB"
    print(msg)
    log_event(f"rotor_disk_report: {msg}")

if __name__ == "__main__":
    report_disk()
