import os

def nlcount_overlay(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if os.path.isfile(path):
        with open(path, "r") as f:
            n = f.read().count("\n")
        print(f"{filename}: {n} newlines")
    else:
        print(f"{filename} not found in overlay.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        nlcount_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_nlcount.py <filename>")
