import os
import subprocess

def test_pipeline(input_file):
    supervisor = os.path.expanduser("~/Soap/agents/pipeline_supervisor.py")
    if not os.path.isfile(supervisor):
        print("Supervisor pipeline not found!")
        return
    subprocess.run(["python3", supervisor, input_file])

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        test_pipeline(sys.argv[1])
    else:
        print("Usage: python pipeline_test_runner.py <sample_input_sop.json>")
