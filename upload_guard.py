# ~/Soap/upload_guard.py

import os
import sys
from pathlib import Path

MAX_GITHUB_MB = 80
MAX_MONGO_MB = 13

GITHUB_EXTS = {".py", ".json", ".js", ".ts", ".md"}
MONGO_EXTS = {".pdf", ".docx", ".txt", ".csv", ".sqlite3"}

def classify_file(file_path):
    ext = Path(file_path).suffix.lower()
    if ext in GITHUB_EXTS:
        return "GitHub"
    elif ext in MONGO_EXTS:
        return "MongoDB"
    else:
        return "GCS"

def get_file_size_mb(file_path):
    return os.path.getsize(file_path) / (1024 * 1024)

def is_within_limit(file_path, limit_mb):
    return get_file_size_mb(file_path) <= limit_mb

def validate_file(file_path):
    if not os.path.exists(file_path):
        return False, "❌ File does not exist."

    kind = classify_file(file_path)
    size_mb = get_file_size_mb(file_path)

    if kind == "GitHub" and not is_within_limit(file_path, MAX_GITHUB_MB):
        return False, f"⛔ {file_path} exceeds GitHub 80MB limit ({size_mb:.2f}MB)."
    elif kind == "MongoDB" and not is_within_limit(file_path, MAX_MONGO_MB):
        return False, f"⛔ {file_path} exceeds MongoDB 13MB limit ({size_mb:.2f}MB)."
    
    return True, f"✅ Ready for {kind} ({size_mb:.2f}MB)"

def main():
    if len(sys.argv) < 2:
        print("📌 Usage:\n  python3 upload_guard.py <file_path>")
        return

    file_path = sys.argv[1]
    ok, message = validate_file(file_path)
    print(message)

if __name__ == "__main__":
    main()
