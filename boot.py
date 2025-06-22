# ~/Soap/boot.py

import subprocess
import os
import time
from pathlib import Path

TRIGGER_PATH = Path.home() / "Soap/.trigger.rebuild"
BOOT_LOG = Path.home() / "Soap/logs/boot.log"

def run(command):
    print(f"⚙️ Running: {command}")
    subprocess.run(command, shell=True, check=True)

def is_running_in_foreground():
    return os.getppid() != 1  # If parent PID is not init, we're not backgrounded

def spawn_background_copy():
    print("🌀 Boot sequence re-spawning in background...")
    BOOT_LOG.parent.mkdir(parents=True, exist_ok=True)
    os.execvp("nohup", ["nohup", "python3", __file__, ">", str(BOOT_LOG), "2>&1", "&"])

def main():
    if is_running_in_foreground():
        spawn_background_copy()
        return  # End foreground parent

    print("🚀 [BOOT] INITIALIZING SYSTEM REACTORS...\n")

    if not TRIGGER_PATH.exists():
        TRIGGER_PATH.touch()
        print("🧠 Wake-up trigger set (.trigger.rebuild)")

    time.sleep(1)
    run("python3 ~/Soap/attention.py")
    time.sleep(1)
    run("python3 ~/Soap/rotor_fusion.py +CODE-RED+")
    time.sleep(1)
    run("python3 ~/Soap/spin_up.py +SPIN-UP+")

    print("🌐 Launching Flask backend...")
    os.chdir("/home/lucasreynolds1988/ati-web-app/backend")
    run("nohup python3 app.py &")

    print("🌐 Opening port 5000 for web preview...")
    run("gcloud cloud-shell ports open 5000")

    print("\n" + "=" * 60)
    print("🧠  SOAP ENGINE IS ONLINE — READY FOR INPUT".center(60))
    print("=" * 60 + "\n")
    print("✅ SYSTEM FULLY BOOTED — SOAP ENGINE ONLINE")

if __name__ == "__main__":
    main()
