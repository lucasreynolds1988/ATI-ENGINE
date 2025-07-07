import os

def status_cli():
    print("=== Rotor System CLI Status ===")
    root = os.path.expanduser("~/Soap")
    print(f"Root: {root}")
    print("Subdirs:")
    for sub in os.listdir(root):
        print(f"  - {sub}")

if __name__ == "__main__":
    status_cli()
