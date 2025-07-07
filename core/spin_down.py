import os
import subprocess
import time
from core.rotor_overlay import log_event

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/lucasreynolds1988/Soap/secrets/gcs-creds.json"

def create_core_backup():
    backup_dir = os.path.expanduser("~/Soap/overlay")
    zip_path = os.path.expanduser("~/Soap/ATI_CORE_SNAPSHOT.zip")
    # Only backup core files and not logs or overlay
    subprocess.run([
        "zip", "-r", zip_path,
        "core", "agents", "admin", "backend", "engine", "install_required_pips.py", "requirements.txt",
        "README_ENGINE_RULES.txt", "+BOOT+", "+START+", "+START+.py", "startup"
    ], cwd=os.path.expanduser("~/Soap"))
    log_event(f"spin_down: Created core backup {zip_path}")
    return zip_path

def upload_backup_gcs(zip_path):
    subprocess.run(["gsutil", "cp", zip_path, "gs://ati-oracle-engine/backups/"], check=True)
    log_event(f"spin_down: Uploaded backup to GCS: {zip_path}")

def purge_nonessential_files():
    preserve = {"core", "secrets", "overlay", "ATI_CORE_SNAPSHOT.zip"}
    root = os.path.expanduser("~/Soap")
    for entry in os.listdir(root):
        if entry not in preserve:
            path = os.path.join(root, entry)
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                subprocess.run(["rm", "-rf", path])
    log_event("spin_down: Purged non-essential files.")

if __name__ == "__main__":
    zip_path = create_core_backup()
    upload_backup_gcs(zip_path)
    time.sleep(2)
    purge_nonessential_files()
