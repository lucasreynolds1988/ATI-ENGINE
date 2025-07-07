import os

def show_lines_overlay(filename, start, end):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "r") as f:
        lines = f.readlines()
    for i in range(start, min(end, len(lines))):
        print(lines[i].rstrip())

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 3:
        show_lines_overlay(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    else:
        print("Usage: python rotor_overlay_lines.py <filename> <start> <end>")
