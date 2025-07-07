import os

def grep_overlay(pattern):
    overlay = os.path.expanduser("~/Soap/overlay")
    for fname in os.listdir(overlay):
        path = os.path.join(overlay, fname)
        if os.path.isfile(path):
            with open(path, "r") as f:
                for line in f:
                    if pattern in line:
                        print(f"{fname}: {line.rstrip()}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        grep_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_grep.py <pattern>")
