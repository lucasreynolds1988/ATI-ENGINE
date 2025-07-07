# ~/Soap/agents/rotor_safety_check.py

import os

def check():
    # Check for dangerous conditions (disk space, missing files, etc.)
    statvfs = os.statvfs('/')
    free_gb = statvfs.f_frsize * statvfs.f_bavail / (1024 * 1024 * 1024)
    if free_gb < 1.0:
        print("Warning: Less than 1GB free disk space!")
    else:
        print(f"Disk space OK: {free_gb:.2f}GB free.")

if __name__ == "__main__":
    check()
