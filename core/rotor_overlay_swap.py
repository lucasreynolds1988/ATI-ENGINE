import os

def swap_overlay(filename, word1, word2):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "r") as f:
        content = f.read()
    content = content.replace(word1, "___TEMP___")
    content = content.replace(word2, word1)
    content = content.replace("___TEMP___", word2)
    with open(path, "w") as f:
        f.write(content)
    print(f"Swapped '{word1}' and '{word2}' in {filename}.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 3:
        swap_overlay(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: python rotor_overlay_swap.py <filename> <word1> <word2>")
