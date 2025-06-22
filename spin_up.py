# ~/Soap/spin_up.py

import subprocess
import time
from pathlib import Path

rotor_files = [
    "rotor_overlay.py",
    "rotor_fusion.py",
    "fusion_restore_v2.py",
]

def run_rotor(path):
    full_path = Path.home() / "Soap" / path
    if full_path.exists():
        subprocess.Popen(
            ["nohup", "python3", str(full_path)],
            stdout=open(Path.home() / "Soap/logs/spin_up.log", "a"),
            stderr=subprocess.STDOUT
        )
        print(f"🚀 Launched: {path}")
    else:
        print(f"❌ Missing: {path}")

def main():
    print("🔧 [SPIN-UP] Activating all rotor systems...")
    for rotor in rotor_files:
        run_rotor(rotor)
        time.sleep(1.25)

    print("✅ All rotors launched. System is spinning.")

if __name__ == "__main__":
    main()
