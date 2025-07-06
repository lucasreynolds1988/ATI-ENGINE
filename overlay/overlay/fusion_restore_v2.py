#!/usr/bin/env python3
import os
import shutil
import time

HOME_DIR = os.path.expanduser("~")
SOAP_DIR = os.path.join(HOME_DIR, "Soap")
BACKUP_DIR = os.path.join(SOAP_DIR, "cloud_backup")

def save_state():
    print("🧭 Saving system state to backup...")
    os.makedirs(BACKUP_DIR, exist_ok=True)
    for item in os.listdir(SOAP_DIR):
        s = os.path.join(SOAP_DIR, item)
        d = os.path.join(BACKUP_DIR, item)
        if os.path.isdir(s):
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)
    print("✅ System state saved to cloud_backup.")

def restore_state():
    print("🧭 Restoring system state from backup...")
    if not os.path.exists(BACKUP_DIR):
        print("❌ No backup found!")
        return
    for item in os.listdir(BACKUP_DIR):
        s = os.path.join(BACKUP_DIR, item)
        d = os.path.join(SOAP_DIR, item)
        if os.path.isdir(s):
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)
    print("✅ System restore complete.")

def main():
    import sys
    if "--save" in sys.argv:
        save_state()
    else:
        restore_state()

if __name__ == "__main__":
    main()
