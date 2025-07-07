# ~/Soap/agents/rotor_timing_sync.py

import time

def sync_cycle(interval=4):
    print("Rotor timing sync starting...")
    while True:
        print("Rotor cycle pulse at", time.strftime("%H:%M:%S"), flush=True)
        time.sleep(interval)

if __name__ == "__main__":
    sync_cycle()

