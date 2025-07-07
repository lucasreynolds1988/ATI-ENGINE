import os

def reverse_overlay(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if os.path.isfile(path):
        with open(path, "r") as f:
            lines = f.readlines()
        for line in reversed(lines):
            print(line.rstrip())
    else:
        print(f"{filename} not found in overlay.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        reverse_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_reverse.py <filename>")
