import time
from pathlib import Path

def heartbeat(agent_name):
    log_dir = Path.home() / "Soap/logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    with open(log_dir / "rotor_pulse_beat.log", "a") as f:
        f.write(f"{agent_name} ALIVE {time.time()}\n")

if __name__ == "__main__":
    while True:
        # --- Place actual arbiter logic here in the future ---
        heartbeat("arbiter")
        print("[arbiter] Heartbeat sent.")
        time.sleep(4)
