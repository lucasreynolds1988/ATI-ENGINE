import os

def pad_overlay(filename, n):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "r") as f:
        lines = f.readlines()
    if len(lines) < n:
        lines += ["\n"] * (n - len(lines))
    with open(path, "w") as f:
        f.writelines(lines)
    print(f"Padded {filename} to {n} lines.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        pad_overlay(sys.argv[1], int(sys.argv[2]))
    else:
        print("Usage: python rotor_overlay_pad.py <filename> <nlines>")
