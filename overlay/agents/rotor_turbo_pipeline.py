import os
import sys
import subprocess
from core.rotor_overlay import log_event

def turbo_pipeline(input_file):
    steps = [
        ("watson", os.path.expanduser("~/Soap/agents/rotor_watson.py")),
        ("father", os.path.expanduser("~/Soap/agents/rotor_father.py")),
        ("mother", os.path.expanduser("~/Soap/agents/rotor_mother.py")),
        ("arbiter", os.path.expanduser("~/Soap/agents/rotor_arbiter.py")),
        ("soap", os.path.expanduser("~/Soap/agents/rotor_soap.py")),
    ]
    files = [input_file]
    procs = []
    for phase, script in steps:
        out_file = f"{input_file}.{phase}.json" if phase != "soap" else f"{input_file}.final.txt"
        proc = subprocess.Popen(["python3", script, files[-1], out_file])
        procs.append(proc)
        files.append(out_file)
    for proc in procs:
        proc.wait()
    log_event(f"TurboPipeline: All rotors finished in parallel (experimental). Output: {files[-1]}")
    print(f"Turbo pipeline (parallel) complete. Final output: {files[-1]}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        turbo_pipeline(sys.argv[1])
    else:
        print("Usage: python rotor_turbo_pipeline.py <raw_input_file>")
