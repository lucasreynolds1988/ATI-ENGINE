import os

def overlay_size():
    overlay = os.path.expanduser("~/Soap/overlay")
    total = 0
    for fname in os.listdir(overlay):
        fpath = os.path.join(overlay, fname)
        if os.path.isfile(fpath):
            total += os.path.getsize(fpath)
    print(f"Overlay size: {total//1024//1024} MB")

if __name__ == "__main__":
    overlay_size()
