# ~/Soap/agents/pipeline_dynamic_runner.py

import sys
import os
import subprocess
import json

def run_all_agents(input_file):
    # Sequence: Watson → Father → Mother → Arbiter → Soap
    # Each agent should accept input_file as arg, produce a JSON or TXT output

    agents = [
        "watson_phase.py",
        "father_phase.py",
        "mother_phase.py",
        "arbiter_phase.py",
        "soap_phase.py"
    ]

    for agent in agents:
        agent_path = os.path.expanduser(f"~/Soap/agents/{agent}")
        if not os.path.isfile(agent_path):
            print(f"Missing agent: {agent_path}", flush=True)
            continue
        print(f"Running {agent} on {input_file}...", flush=True)
        subprocess.run(["python3", agent_path, input_file])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 pipeline_dynamic_runner.py <input_file>")
        sys.exit(1)
    run_all_agents(sys.argv[1])
