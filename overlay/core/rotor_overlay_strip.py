import os

def strip_overlay(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if os.path.isfile(path):
        with open(path, "r") as f:
            lines = f.readlines()
        stripped = [line.strip() for line in lines]
        for line in stripped:
            print(line)
    else:
        print(f"{filename} not found in overlay.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        strip_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_strip.py <filename>")
