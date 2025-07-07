import os

def endswith_overlay(filename, ending):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "r") as f:
        for line in f:
            if line.rstrip().endswith(ending):
                print(line.rstrip())

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        endswith_overlay(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python rotor_overlay_endswith.py <filename> <ending>")
