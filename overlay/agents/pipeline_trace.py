import os

def trace_pipeline(input_file):
    files = [
        f"{input_file}.watson.json",
        f"{input_file}.father.json",
        f"{input_file}.mother.json",
        f"{input_file}.arbiter.json",
        f"{input_file}.final.txt"
    ]
    for f in files:
        exists = os.path.isfile(f)
        print(f"{f}: {'FOUND' if exists else 'missing'}")
        if exists:
            with open(f) as file:
                print("--- Content ---")
                print(file.read())
                print("---------------")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        trace_pipeline(sys.argv[1])
    else:
        print("Usage: python pipeline_trace.py <input_file>")
