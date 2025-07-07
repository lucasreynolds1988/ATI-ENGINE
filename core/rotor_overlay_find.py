import os

def find_file(search_term):
    overlay = os.path.expanduser("~/Soap/overlay")
    matches = []
    for fname in os.listdir(overlay):
        if search_term in fname:
            matches.append(fname)
    if matches:
        for m in matches:
            print(m)
    else:
        print(f"No overlay files match '{search_term}'.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        find_file(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_find.py <search_term>")
