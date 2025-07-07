import os

def split_overlay(filename, nlines):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    nlines = int(nlines)
    with open(path, "r") as f:
        lines = f.readlines()
    for idx in range(0, len(lines), nlines):
        chunk = lines[idx:idx+nlines]
        out = os.path.join(overlay, f"{filename}.part{idx//nlines:03d}")
        with open(out, "w") as f:
            f.writelines(chunk)
        print(f"Created {out}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        split_overlay(sys.argv[1], int(sys.argv[2]))
    else:
        print("Usage: python rotor_overlay_split.py <filename> <nlines>")
