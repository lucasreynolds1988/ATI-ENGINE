import os

def list_overlay():
    overlay = os.path.expanduser("~/Soap/overlay")
    for fname in os.listdir(overlay):
        print(fname)

if __name__ == "__main__":
    list_overlay()
