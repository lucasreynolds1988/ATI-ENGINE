import os
import sys
import subprocess
from core.rotor_overlay import log_event

def run_brancher(input_file, branch="all"):
    """
    Allows running any single agent rotor or all (pipeline style).
    Usage: python eye_brancher.py <input_file> [branch]
    branch: watson, father, mother, arbiter, soap, all (default)
    """
    steps = [
        ("watson", os.path.expanduser("~/Soap/agents/rotor_watson.py")),
        ("father", os.path.expanduser("~/Soap/agents/rotor_father.py")),
        ("mother", os.path.expanduser("~/Soap/agents/rotor_mother.py")),
        ("arbiter", os.path.expanduser("~/Soap/agents/rotor_arbiter.py")),
        ("soap", os.path.expanduser("~/Soap/agents/rotor_soap.py")),
    ]
    files = [input_file]
    for phase, script in steps:
        if branch == "all" or phase == branch:
            out_file = f"{input_file}.{phase}.json" if phase != "soap" else f"{input_file}.final.txt"
            subprocess.run(["python3", script, files[-1], out_file], check=True)
            files.append(out_file)
            if branch != "all":
                print(f"{phase} complete. Output: {out_file}")
                break
    log_event(f"EyeBrancher: Finished {branch} on {input_file}")

if __name__ == "__main__":
    branch = sys.argv[2] if len(sys.argv) > 2 else "all"
    if len(sys.argv) > 1:
        run_brancher(sys.argv[1], branch)
    else:
        print("Usage: python eye_brancher.py <input_file> [branch]")
