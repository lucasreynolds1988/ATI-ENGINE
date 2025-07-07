import os
import subprocess

def run_hook_all(folder, hook):
    files = [f for f in os.listdir(folder) if f.endswith(".json") or f.endswith(".txt")]
    for f in files:
        subprocess.run(["python3", hook, os.path.join(folder, f)])

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        run_hook_all(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python pipeline_run_hook_all.py <folder> <hook_script.py>")
