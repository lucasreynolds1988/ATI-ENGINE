import os

def truncate_overlay(filename, nlines):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if os.path.isfile(path):
        with open(path, "r") as f:
            lines = f.readlines()
        with open(path, "w") as f:
            f.writelines(lines[:nlines])
        print(f"Truncated {filename} to {nlines} lines.")
    else:
        print(f"{filename} not found in overlay.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        truncate_overlay(sys.argv[1], int(sys.argv[2]))
    else:
        print("Usage: python rotor_overlay_truncate.py <filename> <nlines>")
