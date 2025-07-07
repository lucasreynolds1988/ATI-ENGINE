import os

def export_txt(outfile="overlay_export.txt"):
    overlay = os.path.expanduser("~/Soap/overlay")
    with open(outfile, "w") as f:
        for fname in os.listdir(overlay):
            path = os.path.join(overlay, fname)
            sz = os.path.getsize(path)
            mtime = os.path.getmtime(path)
            f.write(f"{fname}\t{sz} bytes\t{mtime}\n")
    print(f"Overlay TXT export complete: {outfile}")

if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "overlay_export.txt"
    export_txt(out)
