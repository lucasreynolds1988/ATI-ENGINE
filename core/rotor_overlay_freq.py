import os
from collections import Counter

def freq_overlay(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if os.path.isfile(path):
        with open(path, "r") as f:
            words = f.read().split()
        counts = Counter(words)
        for word, count in counts.most_common():
            print(f"{word}: {count}")
    else:
        print(f"{filename} not found in overlay.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        freq_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_freq.py <filename>")
