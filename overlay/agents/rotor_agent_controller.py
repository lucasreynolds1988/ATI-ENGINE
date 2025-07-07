# ~/Soap/agents/rotor_agent_controller.py

import os
import time
import subprocess
from pathlib import Path

QUEUE_DIR = Path.home() / "Soap/agent_queue"
os.makedirs(QUEUE_DIR, exist_ok=True)

PHASES = [
    "watson_phase.py",
    "father_phase.py",
    "mother_phase.py",
    "soap_phase.py"
]

def get_tasks():
    return sorted([f for f in QUEUE_DIR.glob("*.json")])

def main():
    print("🔁 [Agent Rotor Controller] Starting...")
    while True:
        tasks = get_tasks()
        if not tasks:
            print("🕒 [Idle] No tasks in queue.")
            time.sleep(4)
            continue

        for phase in PHASES:
            print(f"🌀 Triggering: {phase}")
            subprocess.run(["python3", str(Path(__file__).parent / phase)])
            time.sleep(4)  # spacing between phases

if __name__ == "__main__":
    main()
