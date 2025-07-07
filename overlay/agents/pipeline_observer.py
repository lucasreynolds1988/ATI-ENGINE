import os
import time

def observe(input_file):
    exts = [".watson.json", ".father.json", ".mother.json", ".arbiter.json", ".final.txt"]
    while True:
        print("----- Pipeline File Status -----")
        for ext in exts:
            fname = f"{input_file}{ext}"
            print(f"{fname}: {'FOUND' if os.path.isfile(fname) else 'missing'}")
        print("Refreshing in 5s...")
        time.sleep(5)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        observe(sys.argv[1])
    else:
        print("Usage: python pipeline_observer.py <input_file>")

