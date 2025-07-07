import os
import subprocess
from core.rotor_overlay import log_event

def restore_backup():
    base = os.path.expanduser("~/Soap")
    backup_file = os.path.join(base, "ATI_ROTOR_BACKUP.zip")
    if os.path.isfile(backup_file):
        subprocess.run(["unzip", "-o", backup_file, "-d", base])
        log_event(f"rotor_restore_backup: Restored from {backup_file}")
    else:
        print("Backup file not found.")

if __name__ == "__main__":
    restore_backup()
