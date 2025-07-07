import os
from collections import Counter

def dupcount_overlay(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "r") as f:
        lines = f.readlines()
    counts = Counter(lines)
    dups = [(line.strip(), c) for line, c in counts.items() if c > 1]
    if dups:
        print(f"Duplicate line counts in {filename}:")
        for line, count in dups:
            print(f"{count} x {line}")
    else:
        print(f"No duplicate lines in {filename}.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        dupcount_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_dupcount.py <filename>")
