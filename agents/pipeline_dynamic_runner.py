import os
import sys
import json
import subprocess
import time
from core.rotor_overlay import log_event

CONFIG = os.path.expanduser("~/Soap/agents/pipeline_config.json")

def run_dynamic_pipeline(input_file, role="tech"):
    with open(CONFIG) as f:
        cfg = json.load(f)
    phases = cfg["phases"]
    delay = cfg.get("delay_seconds", 0)
    roles = cfg.get("role_controls", {})
    run_roles = roles.get("run_roles", [])
    if role not in run_roles:
        print(f"Role '{role}' not permitted to run pipeline.")
        return
    files = [input_file]
    for phase in phases:
        script = os.path.expanduser(f"~/Soap/agents/{phase['script']}")
        out_file = f"{input_file}.{phase['name']}.json" if phase['name'] != "soap" else f"{input_file}.final.txt"
        subprocess.run(["python3", script, files[-1], out_file], check=True)
        files.append(out_file)
        if delay:
            time.sleep(delay)
    log_event(f"DynamicPipeline: {input_file} complete. Output: {files[-1]}")
    print(f"Dynamic pipeline complete. Final output: {files[-1]}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        role = sys.argv[2] if len(sys.argv) > 2 else "tech"
        run_dynamic_pipeline(sys.argv[1], role)
    else:
        print("Usage: python pipeline_dynamic_runner.py <input_file> [role]")
