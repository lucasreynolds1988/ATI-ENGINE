import os

def nodup_overlay(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "r") as f:
        lines = f.readlines()
    seen = set()
    with open(path, "w") as f:
        for line in lines:
            if line not in seen:
                f.write(line)
                seen.add(line)
    print(f"Removed duplicate lines from {filename} in overlay.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        nodup_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_nodup.py <filename>")
