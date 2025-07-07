import os
import subprocess
from core.rotor_overlay import log_event

def backup():
    base = os.path.expanduser("~/Soap")
    backup_file = os.path.join(base, "ATI_ROTOR_BACKUP.zip")
    subprocess.run([
        "zip", "-r", backup_file, "core", "agents", "admin", "backend", "engine",
        "install_required_pips.py", "requirements.txt", "README_ENGINE_RULES.txt",
        "+BOOT+", "+START+", "+START+.py", "startup"
    ], cwd=base)
    log_event(f"rotor_backup: Created backup at {backup_file}")

if __name__ == "__main__":
    backup()
