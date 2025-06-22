# ~/Soap/boot.py

import subprocess
import time
from pathlib import Path

def run(command):
    print(f"⚙️ Running: {command}")
    subprocess.run(command, shell=True, check=False)

def main():
    print("🚀 [BOOT] INITIALIZING SYSTEM REACTORS...")

    # GitHub Pull First
    if not Path("/home/lucasreynolds1988/Soap/.git").exists():
        run("git clone https://github.com/lucasr610/Soap.git ~/Soap")
    else:
        run("cd ~/Soap && git pull origin main")

    time.sleep(3)

    # Restore from Mongo + GCS
    run("python3 ~/Soap/fusion_restore_v2.py")
    time.sleep(3)

    # Launch all rotors
    run("python3 ~/Soap/spin_up.py")

if __name__ == "__main__":
    main()
