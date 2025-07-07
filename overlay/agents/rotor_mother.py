import subprocess
import os
from core.rotor_overlay import log_event

def run(input_file, output_file):
    subprocess.run([
        "python3", os.path.expanduser("~/Soap/agents/mother_phase.py"),
        input_file, output_file
    ])
    log_event(f"Rotor-Mother: Completed {input_file} → {output_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        run(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python rotor_mother.py <input_file> <output_file>")
