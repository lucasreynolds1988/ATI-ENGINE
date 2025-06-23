# ~/Soap/agents/agent_sequence_runner.py

import subprocess
import time
from pathlib import Path

AGENT_SEQUENCE = [
    ("watson_phase.py", "watson.log"),
    ("father_phase.py", "father.log"),
    ("mother_phase.py", "mother.log"),
    ("arbiter_phase.py", "arbiter.log"),
    ("soap_phase.py", "soap.log")
]

def run_agent(agent_file, log_file):
    print(f"▶️ Starting {agent_file}")
    with open(Path.home() / "Soap/logs" / log_file, "w") as log:
        process = subprocess.Popen(
            ["python3", str(Path.home() / "Soap/agents" / agent_file)],
            stdout=log,
            stderr=log
        )
        process.wait()
    print(f"✅ Completed {agent_file}")
    time.sleep(2.5)  # ⏱️ Timing delay for rotor coordination

def main():
    for agent, logfile in AGENT_SEQUENCE:
        run_agent(agent, logfile)

if __name__ == "__main__":
    main()
