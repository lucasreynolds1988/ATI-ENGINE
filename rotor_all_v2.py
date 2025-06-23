# ~/Soap/rotor_all_v2.py

import subprocess
import time
from pathlib import Path

LOG_PATH = Path.home() / "Soap/logs/rotor_all_v2.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

ROTORS = {
    "GitHub Sync"       : "rotor_github.py",
    "MongoDB Sync"      : "rotor_mongo.py",
    "GCS Sync"          : "rotor_gcs.py",
    "Fusion Engine"     : "rotor_fusion.py",
    "Timing Chain"      : "rotor_timing_sync.py",
    "SHA Safety Check"  : "rotor_safety_check.py",
    "UI Pulse Sync"     : "rotor_pulse_ui.py",
    "Log Filter"        : "rotor_log_filter.py",
    "Cluster Link"      : "rotor_cluster_link.py"
}

def log(msg):
    with open(LOG_PATH, "a") as f:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {msg}\n")

def launch_rotor(name, script):
    path = Path.home() / "Soap" / script
    if path.exists():
        subprocess.Popen(["nohup", "python3", str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"⚙️ Launching {name} ({script})...")
        log(f"Launched: {script}")
    else:
        print(f"❌ MISSING: {name} ({script})")
        log(f"Missing: {script}")

def main():
    print("🔁 [ROTOR-ALL V2] Launching complete rotor engine stack...\n")
    for name, script in ROTORS.items():
        launch_rotor(name, script)
    print("\n✅ [ROTOR-ALL V2] All rotors are engaged.")
    log("Full rotor engine stack launched.")

if __name__ == "__main__":
    main()
