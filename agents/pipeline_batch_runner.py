import os
import subprocess

def batch_run(folder):
    supervisor = os.path.expanduser("~/Soap/agents/pipeline_supervisor.py")
    files = [f for f in os.listdir(folder) if f.endswith(".json") or f.endswith(".txt")]
    for f in files:
        path = os.path.join(folder, f)
        subprocess.run(["python3", supervisor, path])

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        batch_run(sys.argv[1])
    else:
        print("Usage: python pipeline_batch_runner.py <folder>")
