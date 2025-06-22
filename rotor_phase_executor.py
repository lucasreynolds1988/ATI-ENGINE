# ~/Soap/rotor_timing_chain.py

import time
import subprocess
import threading

ROTOR_CONFIG = {
    "mongo": {"delay": 4.2, "max_mb": 13, "command": ["python3", "mongo_safe_upload_v2.py"]},
    "gcs":   {"delay": 4.4, "max_mb": 20, "command": ["python3", "gcs_safe_upload.py"]},
    "git":   {"delay": 5.0, "max_mb": 40, "command": ["python3", "git_safe_push.py"]},
    "restore": {"delay": 4.6, "max_mb": 40, "command": ["python3", "fusion_restore_v2.py"]},
}

PHASE_OFFSET = 1.2
rotor_log = []

def execute_rotor(rotor_id, config):
    delay = config["delay"]
    command = config["command"]

    while True:
        try:
            start = time.time()
            print(f"🌀 [{rotor_id.upper()}] Rotor spin initiated...")
            subprocess.run(command, check=True)
            elapsed = time.time() - start
            rotor_log.append(f"✅ {rotor_id} ran in {elapsed:.2f}s")
        except subprocess.CalledProcessError as e:
            rotor_log.append(f"❌ {rotor_id} failed: {e}")
        time.sleep(delay)

def spawn_rotors():
    threads = []
    base_time = time.time()
    
    for i, (rotor_id, config) in enumerate(ROTOR_CONFIG.items()):
        offset = PHASE_OFFSET * i
        delay_start = base_time + offset - time.time()
        if delay_start > 0:
            time.sleep(delay_start)

        t = threading.Thread(target=execute_rotor, args=(rotor_id, config), daemon=True)
        t.start()
        threads.append(t)
        print(f"⏱️ [{rotor_id.upper()}] Phase-offset initialized ({offset:.2f}s)")

    return threads

def display_rotor_log():
    print("\n📘 Rotor Log Summary:")
    for entry in rotor_log[-20:]:
        print(" -", entry)

def main():
    print("🚀 Rotor Timing Chain Initialized...")
    threads = spawn_rotors()

    try:
        while True:
            time.sleep(15)
            display_rotor_log()
    except KeyboardInterrupt:
        print("\n🛑 Rotor Timing Chain interrupted by user.")

if __name__ == "__main__":
    main()
