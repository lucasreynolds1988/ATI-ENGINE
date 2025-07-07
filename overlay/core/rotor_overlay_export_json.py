import os
import json

def export_json(outfile="overlay_export.json"):
    overlay = os.path.expanduser("~/Soap/overlay")
    data = []
    for fname in os.listdir(overlay):
        path = os.path.join(overlay, fname)
        sz = os.path.getsize(path)
        mtime = os.path.getmtime(path)
        data.append({"filename": fname, "size": sz, "mtime": mtime})
    with open(outfile, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Overlay JSON export complete: {outfile}")

if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "overlay_export.json"
    export_json(out)
