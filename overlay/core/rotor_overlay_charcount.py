import os

def charcount_overlay(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if os.path.isfile(path):
        with open(path, "r") as f:
            content = f.read()
            print(f"{filename}: {len(content)} characters")
    else:
        print(f"{filename} not found in overlay.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        charcount_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_charcount.py <filename>")
