# ~/Soap/agents/rotor_pulse_ui.py

import time
import sys

def pulse():
    for i in range(5):
        print(f"Rotor Pulse {i+1}: {'💓' if i % 2 == 0 else '💢'}", flush=True)
        time.sleep(1)
    print("Rotor Pulse Complete.")

if __name__ == "__main__":
    pulse()
