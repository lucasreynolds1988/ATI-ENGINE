import os
import subprocess

def fanout(input_file, scripts):
    for script in scripts:
        out_file = f"{input_file}.{os.path.basename(script).replace('.py','')}.out"
        subprocess.Popen(["python3", script, input_file, out_file])
    print("Fanout: launched all scripts asynchronously.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        scripts = sys.argv[2:]
        fanout(sys.argv[1], scripts)
    else:
        print("Usage: python eye_pipeline_fanout.py <input_file> <script1.py> <script2.py> ...")
