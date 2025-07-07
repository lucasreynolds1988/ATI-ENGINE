import os

def findlen_overlay(filename, length):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "r") as f:
        for line in f:
            if len(line.strip()) == length:
                print(line.rstrip())

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        findlen_overlay(sys.argv[1], int(sys.argv[2]))
    else:
        print("Usage: python rotor_overlay_findlen.py <filename> <length>")
