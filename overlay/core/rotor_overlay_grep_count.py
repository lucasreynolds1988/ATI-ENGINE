import os

def grep_count_overlay(filename, word):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "r") as f:
        lines = f.readlines()
    count = sum(1 for line in lines if word in line)
    print(f"{filename}: {count} lines contain '{word}'.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        grep_count_overlay(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python rotor_overlay_grep_count.py <filename> <word>")
