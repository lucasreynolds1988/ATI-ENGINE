# ~/Soap/boot.py

import subprocess
import os
import time

def run(command):
    print(f"⚙️ Running: {command}")
    subprocess.run(command, shell=True, check=True)

def main():
    print("🚀 [BOOT] INITIALIZING SYSTEM REACTORS...\n")
    
    # 1. Wake system
    if not os.path.exists("/home/lucasreynolds1988/Soap/.trigger.rebuild"):
        open("/home/lucasreynolds1988/Soap/.trigger.rebuild", "w").close()
        print("🧠 Wake-up trigger set (.trigger.rebuild)")

    # 2. Run full reactivation sequence
    run("python3 /home/lucasreynolds1988/Soap/attention.py")
    time.sleep(2)

    run("python3 /home/lucasreynolds1988/Soap/rotor_fusion.py +CODE-RED+")
    time.sleep(2)

    run("python3 /home/lucasreynolds1988/Soap/spin_up.py +SPIN-UP+")
    time.sleep(2)

    # 3. Launch backend API
    print("🌐 Launching Flask backend...")
    os.chdir("/home/lucasreynolds1988/ati-web-app/backend")
    run("nohup python3 app.py &")

    # 4. Expose port 5000 for Cloud Shell preview
    print("🌐 Opening port 5000 for web preview...")
    run("gcloud cloud-shell ports open 5000")

    # 5. Status bar
    print("\n" + "=" * 60)
    print("🧠  SOAP ENGINE IS ONLINE — READY FOR INPUT".center(60))
    print("=" * 60 + "\n")

    print("✅ SYSTEM FULLY BOOTED — SOAP ENGINE ONLINE")
    print("🧠 Access frontend: https://shell.cloud.google.com/cloudshell/editor?cloudshell_open_in_editor=true&cloudshell_workspace=~/ati-web-app/frontend")
    print("🌍 Or use the Cloud Shell web preview tab")

if __name__ == "__main__":
    main()
