# status_check.py

import os

def check_dir(path):
    return os.path.exists(os.path.expanduser(path))

def check_module(name):
    try:
        __import__(name)
        return True
    except ImportError:
        return False

def main():
    print("🔎 SYSTEM CHECK REPORT")
    checks = {
        "Soap Directory": check_dir("~/Soap"),
        "ATI Web App": check_dir("~/ati-web-app"),
        "Frontend Dir": check_dir("~/ati-web-app/frontend"),
        "Backend Dir": check_dir("~/ati-web-app/backend"),
        "Logs Dir": check_dir("~/Soap/data/logs"),
        "MongoDB Module": check_module("pymongo"),
        "Git Config": os.system("git status > /dev/null 2>&1") == 0
    }

    for item, result in checks.items():
        status = "✅ OK" if result else "❌ MISSING"
        print(f"{item:<20}: {status}")

if __name__ == "__main__":
    main()
