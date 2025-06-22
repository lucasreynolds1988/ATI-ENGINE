~/Soap/pulse_engine.py

import time
import threading

# Time interval in seconds between pulses (e.g., Mongo -> GCS -> GitHub)
PULSE_INTERVAL = 4
ROTORS = ["MongoDB", "GCS", "GitHub"]

# Optional: shared status tracking
tick_count = 0
status_log = []


def pulse_cycle():
    global tick_count
    print("🫀 Pulse engine online. Rotating access...")
    while True:
        current_rotor = ROTORS[tick_count % len(ROTORS)]
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"🌀 [{timestamp}] ⏱️ Rotating to: {current_rotor}")
        status_log.append({"time": timestamp, "target": current_rotor})

        # Optional: write to shared status file
        try:
            with open("~/Soap/data/logs/pulse_status.json", "w") as f:
                json.dump(status_log[-50:], f, indent=2)  # keep last 50
        except:
            pass

        tick_count += 1
        time.sleep(PULSE_INTERVAL)


def start_pulse_engine():
    pulse_thread = threading.Thread(target=pulse_cycle, daemon=True)
    pulse_thread.start()
    print("🚦 Pulse engine started in background.")


if __name__ == "__main__":
    start_pulse_engine()
    while True:
        time.sleep(60)
