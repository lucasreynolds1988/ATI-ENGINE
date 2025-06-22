# ~/Soap/spin_down.py

import os
import subprocess
import time
from pathlib import Path

def stop_rotors():
    print("🛑 Stopping rotor processes...")
    os.system("pkill -f rotor_overlay.py")
    os.system("pkill -f rotor_fusion.py")
    os.system("pkill -f fusion_restore_v2.py")
    os.system("pkill -f spin_up.py")
    time.sleep(1)

def push_to_github():
    print("⬆️ Final GitHub push...")
    repo_path = Path.home() / "Soap"
    subprocess.run(["git", "-C", str(repo_path), "add", "."], check=False)
    subprocess.run(["git", "-C", str(repo_path), "commit", "-m", "🔒 Safe shutdown commit"], check=False)
    subprocess.run(["git", "-C", str(repo_path), "push"], check=False)

def sync_to_gcs():
    print("☁️ Syncing entire Soap folder to GCS...")
    subprocess.run(["gsutil", "-m", "cp", "-r", str(Path.home() / "Soap"), "gs://ati-rotor-fusion/Soap_backup"], check=False)

def main():
    print("🔻 [+SPIN-DOWN+] INITIATED...")
    stop_rotors()
    push_to_github()
    sync_to_gcs()
    print("✅ All systems safely shut down.")

if __name__ == "__main__":
    main()
