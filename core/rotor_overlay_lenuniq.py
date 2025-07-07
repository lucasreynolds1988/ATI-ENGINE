import os

def lenuniq_overlay(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "r") as f:
        unique = set(f.readlines())
    print(f"{filename}: {len(unique)} unique lines")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        lenuniq_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_lenuniq.py <filename>")
