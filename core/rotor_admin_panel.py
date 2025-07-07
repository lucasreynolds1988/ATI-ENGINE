import subprocess
from core.rotor_overlay import log_event

def open_panel():
    log_event("rotor_admin_panel: Opening admin panel (shell mode).")
    subprocess.call(["/bin/bash"])

if __name__ == "__main__":
    open_panel()
