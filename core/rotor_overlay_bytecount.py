import os

def bytecount_overlay(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if os.path.isfile(path):
        print(f"{filename}: {os.path.getsize(path)} bytes")
    else:
        print(f"{filename} not found in overlay.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        bytecount_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_bytecount.py <filename>")
