import os

def show_overlay():
    overlay = os.path.expanduser("~/Soap/overlay")
    for fname in os.listdir(overlay):
        fpath = os.path.join(overlay, fname)
        if os.path.isfile(fpath):
            print(fname)

if __name__ == "__main__":
    show_overlay()
