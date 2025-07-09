import os
import json

BASE = os.path.expanduser("~/Soap")
MANIFEST_PATH = os.path.join(BASE, "overlay/manifest.json")

def load_protected_paths():
    if not os.path.exists(MANIFEST_PATH):
        return set(), set()
    with open(MANIFEST_PATH, "r") as f:
        try:
            data = json.load(f)
            files = set()
            dirs = set()
            for entry in data:
                path = os.path.expanduser(entry["path"])
                if os.path.isdir(path):
                    dirs.add(path)
                else:
                    files.add(path)
            return files, dirs
        except Exception as e:
            print(f"Error loading manifest: {e}")
            return set(), set()

def is_protected(path, protected_files, protected_dirs):
    if path in protected_files:
        return True
    for d in protected_dirs:
        if path.startswith(d + os.sep):
            return True
    return False

def main():
    protected_files, protected_dirs = load_protected_paths()
    at_risk = []
    protected = []

    for root, _, files in os.walk(BASE):
        for f in files:
            full_path = os.path.join(root, f)
            if is_protected(full_path, protected_files, protected_dirs):
                protected.append(full_path)
            else:
                at_risk.append(full_path)

    print("🔒 Scanning for protected vs at-risk files...\n")
    print(f"✅ Protected files: {len(protected)}")
    print(f"⚠️  At-risk files: {len(at_risk)}\n")

    if at_risk:
        print("⚠️ Files NOT covered by protection rules:")
        for f in sorted(at_risk):
            print(" -", f.replace(BASE + os.sep, ""))
    else:
        print("🎉 All files are protected.")

if __name__ == "__main__":
    main()
import os
import json

BASE = os.path.expanduser("~/Soap")
MANIFEST_PATH = os.path.join(BASE, "overlay/manifest.json")

def load_protected_paths():
    if not os.path.exists(MANIFEST_PATH):
        return set(), set()
    with open(MANIFEST_PATH, "r") as f:
        try:
            data = json.load(f)
            files = set()
            dirs = set()
            for entry in data:
                path = os.path.expanduser(entry["path"])
                if os.path.isdir(path):
                    dirs.add(path)
                else:
                    files.add(path)
            return files, dirs
        except Exception as e:
            print(f"Error loading manifest: {e}")
            return set(), set()

def is_protected(path, protected_files, protected_dirs):
    if path in protected_files:
        return True
    for d in protected_dirs:
        if path.startswith(d + os.sep):
            return True
    return False

def main():
    protected_files, protected_dirs = load_protected_paths()
    at_risk = []
    protected = []

    for root, _, files in os.walk(BASE):
        for f in files:
            full_path = os.path.join(root, f)
            if is_protected(full_path, protected_files, protected_dirs):
                protected.append(full_path)
            else:
                at_risk.append(full_path)

    print("🔒 Scanning for protected vs at-risk files...\n")
    print(f"✅ Protected files: {len(protected)}")
    print(f"⚠️  At-risk files: {len(at_risk)}\n")

    if at_risk:
        print("⚠️ Files NOT covered by protection rules:")
        for f in sorted(at_risk):
            print(" -", f.replace(BASE + os.sep, ""))
    else:
        print("🎉 All files are protected.")

if __name__ == "__main__":
    main()
