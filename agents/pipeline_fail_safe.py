import os
import subprocess

def run_with_failover(input_file):
    try:
        subprocess.run([
            "python3", os.path.expanduser("~/Soap/agents/pipeline_supervisor.py"),
            input_file
        ], check=True)
    except Exception as e:
        print("Pipeline failed. Attempting re-run...")
        subprocess.run([
            "python3", os.path.expanduser("~/Soap/agents/pipeline_supervisor.py"),
            input_file
        ])

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        run_with_failover(sys.argv[1])
    else:
        print("Usage: python pipeline_fail_safe.py <input_file>")
