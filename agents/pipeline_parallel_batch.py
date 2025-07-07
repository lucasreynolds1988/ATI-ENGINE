import os
import subprocess
from multiprocessing import Pool

def process_file(path):
    supervisor = os.path.expanduser("~/Soap/agents/pipeline_supervisor.py")
    subprocess.run(["python3", supervisor, path])

def parallel_batch(folder, n=4):
    files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".json") or f.endswith(".txt")]
    with Pool(n) as pool:
        pool.map(process_file, files)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 4
        parallel_batch(sys.argv[1], n)
    else:
        print("Usage: python pipeline_parallel_batch.py <folder> [n_processes]")
