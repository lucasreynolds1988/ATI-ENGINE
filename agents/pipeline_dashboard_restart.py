import os
import subprocess

def restart_pipeline(input_file):
    subprocess.Popen([
        "python3",
        os.path.expanduser("~/Soap/agents/pipeline_dynamic_runner.py"),
        input_file
    ])
    print(f"Restarted pipeline for {input_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        restart_pipeline(sys.argv[1])
    else:
        print("Usage: python pipeline_dashboard_restart.py <input_file>")
