import os

def head_tail_overlay(filename, head=5, tail=5):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "r") as f:
        lines = f.readlines()
    print("--- HEAD ---")
    for line in lines[:head]:
        print(line.rstrip())
    print("--- TAIL ---")
    for line in lines[-tail:]:
        print(line.rstrip())

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        head_tail_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_head_tail.py <filename>")
