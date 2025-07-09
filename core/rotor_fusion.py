# ~/Soap/core/rotor_fusion.py

import os
from core.cloud_stream_relay import execute_relay_cycle
from core.rotor_overlay import log_event

def main():
    log_event("[ROTOR-FUSION] 🔄 Rotor cycle triggered.")
    relay_dir = os.path.expanduser("~/Soap/relay/")
    if not os.path.exists(relay_dir):
        log_event("[ROTOR-FUSION] ⚠️ Relay dir missing.")
        return

    for file in os.listdir(relay_dir):
        file_path = os.path.join(relay_dir, file)
        execute_relay_cycle(file_path)

    log_event("[ROTOR-FUSION] ✅ Cycle complete.")

if __name__ == "__main__":
    main()
