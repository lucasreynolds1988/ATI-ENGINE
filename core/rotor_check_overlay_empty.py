import os

def overlay_empty():
    overlay = os.path.expanduser("~/Soap/overlay")
    is_empty = len(os.listdir(overlay)) == 0
    print("Overlay is empty." if is_empty else "Overlay is NOT empty.")

if __name__ == "__main__":
    overlay_empty()
