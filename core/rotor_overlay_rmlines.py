import os

def rmlines_overlay(filename, start, end):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "r") as f:
        lines = f.readlines()
    with open(path, "w") as f:
        f.writelines(lines[:start] + lines[end:])
    print(f"Removed lines {start} to {end-1} from {filename}.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 3:
        rmlines_overlay(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    else:
        print("Usage: python rotor_overlay_rmlines.py <filename> <start> <end>")
