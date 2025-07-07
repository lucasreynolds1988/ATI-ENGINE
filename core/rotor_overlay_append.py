import os

def append_overlay(filename, text):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    with open(path, "a") as f:
        f.write(text + "\n")
    print(f"Appended to {filename} in overlay.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        append_overlay(sys.argv[1], " ".join(sys.argv[2:]))
    else:
        print("Usage: python rotor_overlay_append.py <filename> <text>")
