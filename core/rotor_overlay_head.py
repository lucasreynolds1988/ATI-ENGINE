import os

def head_overlay(filename, lines=10):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if os.path.isfile(path):
        with open(path, "r") as f:
            for i, line in enumerate(f):
                if i >= lines:
                    break
                print(line.rstrip())
    else:
        print(f"{filename} not found in overlay.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        head_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_head.py <filename>")
