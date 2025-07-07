import os

def isascii_overlay(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "rb") as f:
        try:
            content = f.read()
            if content.isascii():
                print(f"{filename} is ASCII.")
            else:
                print(f"{filename} is NOT ASCII.")
        except Exception as e:
            print(f"Error reading {filename}: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        isascii_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_isascii.py <filename>")
