import os
import random

def sample_overlay(filename, n):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "r") as f:
        lines = f.readlines()
    n = min(n, len(lines))
    for line in random.sample(lines, n):
        print(line.rstrip())

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        sample_overlay(sys.argv[1], int(sys.argv[2]))
    else:
        print("Usage: python rotor_overlay_sample.py <filename> <nlines>")
