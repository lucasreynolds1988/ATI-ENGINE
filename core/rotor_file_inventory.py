import os
from core.rotor_overlay import log_event

def make_inventory():
    root = os.path.expanduser("~/Soap")
    inventory_file = os.path.join(root, "_file_inventory.txt")
    with open(inventory_file, "w") as out:
        for dirpath, _, files in os.walk(root):
            for f in files:
                out.write(os.path.relpath(os.path.join(dirpath, f), root) + "\n")
    log_event(f"rotor_file_inventory: Wrote file inventory to {inventory_file}")

if __name__ == "__main__":
    make_inventory()
