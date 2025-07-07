import os
import subprocess
from multiprocessing import Process

def run_parallel(input_file):
    scripts = [
        os.path.expanduser("~/Soap/agents/rotor_watson.py"),
        os.path.expanduser("~/Soap/agents/rotor_father.py"),
        os.path.expanduser("~/Soap/agents/rotor_mother.py"),
        os.path.expanduser("~/Soap/agents/rotor_arbiter.py"),
        os.path.expanduser("~/Soap/agents/rotor_soap.py"),
    ]
    procs = []
    for script in scripts:
        out_file = f"{input_file}.{os.path.basename(script).replace('rotor_','').replace('.py','')}.out"
        p = Process(target=subprocess.run, args=(["python3", script, input_file, out_file],))
        procs.append(p)
        p.start()
    for p in procs:
        p.join()
    print("All eye branches run in parallel.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        run_parallel(sys.argv[1])
    else:
        print("Usage: python eye_parallel_branch.py <input_file>")
