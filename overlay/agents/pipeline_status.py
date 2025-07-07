import os

def status(input_file):
    exts = [".watson.json", ".father.json", ".mother.json", ".arbiter.json", ".final.txt"]
    for ext in exts:
        fname = f"{input_file}{ext}"
        exists = os.path.isfile(fname)
        print(f"{fname}: {'FOUND' if exists else 'missing'}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        status(sys.argv[1])
    else:
        print("Usage: python pipeline_status.py <input_file>")
