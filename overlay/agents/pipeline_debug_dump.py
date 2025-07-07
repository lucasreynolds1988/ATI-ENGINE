import os

def dump_all(input_file):
    exts = [".watson.json", ".father.json", ".mother.json", ".arbiter.json", ".final.txt"]
    for ext in exts:
        fname = f"{input_file}{ext}"
        if os.path.isfile(fname):
            print(f"=== {fname} ===")
            with open(fname) as f:
                print(f.read())

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        dump_all(sys.argv[1])
    else:
        print("Usage: python pipeline_debug_dump.py <input_file>")
