import os
import subprocess

def run_pipeline_with_error_hook(input_file, error_hook):
    try:
        subprocess.run([
            "python3", os.path.expanduser("~/Soap/agents/pipeline_supervisor.py"),
            input_file
        ], check=True)
    except Exception as e:
        print("Pipeline failed. Running error hook...")
        subprocess.run(["python3", error_hook, input_file])

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        run_pipeline_with_error_hook(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python pipeline_error_hook.py <input_file> <error_hook.py>")
