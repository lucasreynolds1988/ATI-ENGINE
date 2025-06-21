# ~/Soap/spin_up.py

import os
import subprocess
import time

def run_fusion_check():
    print("🔎 SYSTEM CHECK REPORT")

    checks = {
        "Soap Directory": "~/Soap",
        "ATI Web App": "~/ati-web-app",
        "Frontend Dir": "~/ati-web-app/frontend",
        "Backend Dir": "~/ati-web-app/backend",
        "Logs Dir": "~/Soap/data/logs",
        "MongoDB Module": "~/.local/lib/python*/site-packages/pymongo",
        "Git Config": "~/.gitconfig"
    }

    for label, path in checks.items():
        expanded = os.path.expanduser(path.replace("*", ""))
        exists = os.path.exists(expanded)
        print(f"{label:<20}: {'✅ OK' if exists else '❌ MISSING'}")

def launch_rotor_core():
    print("[+SPIN-UP+] ROTOR STATUS: 🌀 Starting Rotor Core Synchronization Loop")
    try:
        subprocess.run(["python3", os.path.expanduser("~/Soap/rotor_fusion.py")], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[Rotor Error] ❌ Rotor fusion failed: {e}")
        print("[+SPIN-UP+] ROTOR STATUS: ⏳ Sleeping 4 seconds before next cycle")
        time.sleep(4)
        launch_rotor_core()

def main():
    print("✨ Initializing +SPIN-UP+ trigger...")
    run_fusion_check()
    launch_rotor_core()
    print("✅ +SPIN-UP+ SEQUENCE COMPLETE")

if __name__ == "__main__":
    main()
