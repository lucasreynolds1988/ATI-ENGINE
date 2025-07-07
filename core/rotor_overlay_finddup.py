import os

def finddup_overlay(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "r") as f:
        lines = f.readlines()
    seen = set()
    dups = set()
    for line in lines:
        if line in seen:
            dups.add(line)
        else:
            seen.add(line)
    if dups:
        print(f"Duplicate lines in {filename}:")
        for line in dups:
            print(line.rstrip())
    else:
        print(f"No duplicate lines in {filename}.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        finddup_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_finddup.py <filename>")
