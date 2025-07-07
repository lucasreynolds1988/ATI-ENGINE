import os
import csv

def export_csv(outfile="overlay_export.csv"):
    overlay = os.path.expanduser("~/Soap/overlay")
    with open(outfile, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["filename", "size", "mtime"])
        for fname in os.listdir(overlay):
            path = os.path.join(overlay, fname)
            sz = os.path.getsize(path)
            mtime = os.path.getmtime(path)
            writer.writerow([fname, sz, mtime])
    print(f"Overlay CSV export complete: {outfile}")

if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "overlay_export.csv"
    export_csv(out)
