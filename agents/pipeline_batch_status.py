import os

def batch_status(folder):
    files = [f for f in os.listdir(folder) if f.endswith(".json") or f.endswith(".txt")]
    for f in files:
        exts = [".watson.json", ".father.json", ".mother.json", ".arbiter.json", ".final.txt"]
        status = []
        for ext in exts:
            fname = os.path.join(folder, f + ext) if not f.endswith(ext) else f
            exists = os.path.isfile(fname)
            status.append(f"{os.path.basename(fname)}: {'FOUND' if exists else 'missing'}")
        print(f"\nFile: {f}")
        for s in status:
            print(" ", s)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        batch_status(sys.argv[1])
    else:
        print("Usage: python pipeline_batch_status.py <folder>")
