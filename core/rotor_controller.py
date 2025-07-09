# ~/Soap/core/rotor_controller.py

import os
import time
from core.rotor_overlay import log_event
from core.rotor_fusion import main as fusion_cycle

def start_rotor_loop(interval_seconds=4):
    log_event("[ROTOR-CONTROLLER] 🧭 Starting timed rotor loop...")

    while True:
        try:
            fusion_cycle()
            time.sleep(interval_seconds)
        except KeyboardInterrupt:
            log_event("[ROTOR-CONTROLLER] ❌ Interrupted by user.")
            break
        except Exception as e:
            log_event(f"[ROTOR-CONTROLLER] ⚠️ Error: {str(e)}")
            time.sleep(10)

if __name__ == "__main__":
    start_rotor_loop()
