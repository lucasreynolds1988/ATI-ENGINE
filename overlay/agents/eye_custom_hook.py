import os
import sys

def run_hook(input_file, hook_script):
    # Runs a custom Python hook in the agent pipeline
    os.system(f"python3 {hook_script} {input_file}")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        run_hook(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python eye_custom_hook.py <input_file> <hook_script.py>")
