import os

def batch_find_replace(find_text, replace_text):
    overlay = os.path.expanduser("~/Soap/overlay")
    count = 0
    for fname in os.listdir(overlay):
        path = os.path.join(overlay, fname)
        if os.path.isfile(path):
            with open(path, "r") as f:
                content = f.read()
            if find_text in content:
                content = content.replace(find_text, replace_text)
                with open(path, "w") as f:
                    f.write(content)
                print(f"Replaced in {fname}")
                count += 1
    print(f"Replaced text in {count} overlay files.")

def batch_rename(old, new):
    overlay = os.path.expanduser("~/Soap/overlay")
    renamed = 0
    for fname in os.listdir(overlay):
        if old in fname:
            newname = fname.replace(old, new)
            os.rename(os.path.join(overlay, fname), os.path.join(overlay, newname))
            print(f"Renamed {fname} -> {newname}")
            renamed += 1
    print(f"Renamed {renamed} overlay files.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 4 and sys.argv[1] == "replace":
        batch_find_replace(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 4 and sys.argv[1] == "rename":
        batch_rename(sys.argv[2], sys.argv[3])
    else:
        print("Usage:")
        print("  python rotor_overlay_batch_edit.py replace <find> <replace>")
        print("  python rotor_overlay_batch_edit.py rename <old> <new>")
