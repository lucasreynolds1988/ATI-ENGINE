import os
import random

def shuffle_overlay(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "r") as f:
        lines = f.readlines()
    random.shuffle(lines)
    with open(path, "w") as f:
        f.writelines(lines)
    print(f"Shuffled all lines in {filename}.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        shuffle_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_shuffle.py <filename>")
