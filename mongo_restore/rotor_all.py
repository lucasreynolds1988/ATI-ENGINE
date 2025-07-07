# ~/Soap/rotor_all.py

import subprocess
import time
from pathlib import Path

LOG_PATH = Path.home() / "Soap/logs/rotor_all.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

ROTORS = {
    "GitHub": "rotor_github.py",
    "MongoDB": "rotor_mongo.py",
    "GCS": "rotor_gcs.py"
}

def log(message):
    with open(LOG_PATH, "a") as f:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {message}\n")

def launch_rotor(name, script):
    full_path = Path.home() / "Soap" / script
    if full_path.exists():
        subprocess.Popen(["nohup", "python3", str(full_path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"⚙️ Launching {name} rotor...")
        log(f"Launched: {script}")
    else:
        print(f"❌ {name} rotor missing: {script}")
        log(f"Missing: {script}")

def main():
    print("🔄 [ROTOR-ALL] Starting all background rotors...\n")
    for name, script in ROTORS.items():
        launch_rotor(name, script)
    print("\n✅ [ROTOR-ALL] All rotors launched.")
    log("All rotors launched.")

if __name__ == "__main__":
    main()
