import os

def delete_line_overlay(filename, lineno):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "r") as f:
        lines = f.readlines()
    if 0 <= lineno < len(lines):
        del lines[lineno]
        with open(path, "w") as f:
            f.writelines(lines)
        print(f"Deleted line {lineno} from {filename}")
    else:
        print(f"Invalid line number {lineno}.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        delete_line_overlay(sys.argv[1], int(sys.argv[2]))
    else:
        print("Usage: python rotor_overlay_delete_line.py <filename> <lineno>")
