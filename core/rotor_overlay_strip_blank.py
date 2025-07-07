import os

def strip_blank_overlay(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "r") as f:
        lines = f.readlines()
    notblank = [line for line in lines if line.strip()]
    with open(path, "w") as f:
        f.writelines(notblank)
    print(f"Stripped blank lines from {filename}.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        strip_blank_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_strip_blank.py <filename>")
