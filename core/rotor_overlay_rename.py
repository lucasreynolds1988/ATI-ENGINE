import os

def rename_overlay(old, new):
    overlay = os.path.expanduser("~/Soap/overlay")
    old_path = os.path.join(overlay, old)
    new_path = os.path.join(overlay, new)
    if os.path.isfile(old_path):
        os.rename(old_path, new_path)
        print(f"Renamed {old} to {new} in overlay.")
    else:
        print(f"{old} not found in overlay.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        rename_overlay(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python rotor_overlay_rename.py <old_name> <new_name>")
