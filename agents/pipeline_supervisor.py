import os
import sys
from core.rotor_overlay import log_event
import subprocess

def run_pipeline(input_file):
    # Set up intermediate files
    steps = [
        ("watson", os.path.expanduser("~/Soap/agents/rotor_watson.py")),
        ("father", os.path.expanduser("~/Soap/agents/rotor_father.py")),
        ("mother", os.path.expanduser("~/Soap/agents/rotor_mother.py")),
        ("arbiter", os.path.expanduser("~/Soap/agents/rotor_arbiter.py")),
        ("soap", os.path.expanduser("~/Soap/agents/rotor_soap.py")),
    ]
    files = [input_file]
    for phase, script in steps:
        out_file = f"{input_file}.{phase}.json" if phase != "soap" else f"{input_file}.final.txt"
        subprocess.run(["python3", script, files[-1], out_file], check=True)
        files.append(out_file)
    log_event(f"Pipeline: Complete. Final output: {files[-1]}")
    print(f"Pipeline complete. Final output: {files[-1]}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_pipeline(sys.argv[1])
    else:
        print("Usage: python pipeline_supervisor.py <raw_input_file>")

