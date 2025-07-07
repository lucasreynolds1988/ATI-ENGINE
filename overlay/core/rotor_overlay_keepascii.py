import os

def keepascii_overlay(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    ascii_lines = [line for line in lines if all(ord(char) < 128 for char in line)]
    with open(path, "w") as f:
        f.writelines(ascii_lines)
    print(f"Kept only ASCII lines in {filename}.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        keepascii_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_keepascii.py <filename>")
