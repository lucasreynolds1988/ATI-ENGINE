import os

def clean_pipeline_files(input_file):
    exts = [".watson.json", ".father.json", ".mother.json", ".arbiter.json", ".final.txt"]
    for ext in exts:
        fname = f"{input_file}{ext}"
        if os.path.isfile(fname):
            os.remove(fname)
            print(f"Removed: {fname}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        clean_pipeline_files(sys.argv[1])
    else:
        print("Usage: python pipeline_cleaner.py <input_file>")
