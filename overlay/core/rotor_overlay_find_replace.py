import os

def find_replace_overlay(filename, find_text, replace_text):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if os.path.isfile(path):
        with open(path, "r") as f:
            lines = f.readlines()
        count = 0
        with open(path, "w") as f:
            for line in lines:
                if find_text in line:
                    line = line.replace(find_text, replace_text)
                    count += 1
                f.write(line)
        print(f"Replaced {count} occurrence(s) of '{find_text}' in {filename}.")
    else:
        print(f"{filename} not found in overlay.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 3:
        find_replace_overlay(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: python rotor_overlay_find_replace.py <filename> <find_text> <replace_text>")
