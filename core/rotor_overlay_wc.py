import os

def wc_overlay(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if os.path.isfile(path):
        with open(path, "r") as f:
            text = f.read()
            words = len(text.split())
            lines = text.count("\n") + 1
            chars = len(text)
        print(f"{filename}: {lines} lines, {words} words, {chars} chars")
    else:
        print(f"{filename} not found in overlay.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        wc_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_wc.py <filename>")
