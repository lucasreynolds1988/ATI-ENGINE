# ~/Soap/status_check.py

import os
import shutil
import subprocess
import importlib.util

def run(command):
    """Run shell command and return output as string."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def check_file(path):
    return os.path.isfile(path)

def check_dir(path):
    return os.path.isdir(path)

def check_command(cmd):
    return shutil.which(cmd) is not None

def check_python_package(package):
    return importlib.util.find_spec(package) is not None

def check_gcs_bucket(bucket_url):
    try:
        result = subprocess.run(f"gsutil ls {bucket_url}", shell=True, capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def status(label, passed):
    mark = "✅" if passed else "❌"
    print(f"{mark} {label}")

# 1. Cache Files
print("\n🧠 ROTOR MEMORY CHECK")
status(".rotor-cache.json", check_file(".rotor-cache.json"))
status(".fusion-log.json", check_file(".fusion-log.json"))

# 2. Directory Check
print("\n📁 DIRECTORY STRUCTURE")
status("Soap", check_dir("."))
status("manuals/", check_dir("manuals"))
status("logs/", check_dir("logs"))
status("data/logs/", check_dir("data/logs"))
status("frontend/", check_dir("frontend"))
status("backend/", check_dir("backend"))
status("vectorizer/", check_dir("vectorizer"))

# 3. Cloud + Remote
print("\n☁️ REMOTE CONNECTIVITY")
status("Git Installed", check_command("git"))
status("gsutil Access", check_gcs_bucket("gs://ati-rotor-storage/"))
status("MongoDB Driver (pymongo)", check_python_package("pymongo"))

# 4. Disk Usage with Live Report
print("\n💽 DISK USAGE")
total, used, free = shutil.disk_usage("/home")
status("Home Free Space > 500MB", free > 500 * 1024 * 1024)

print("\n📦 Disk Usage:")
print(run("df -h / /home /root"))

print("\n📁 Directory Sizes (Top Level):")
print(run("du -h --max-depth=1 ~ | sort -hr | head -n 20"))

print("\n🐘 Top 10 Largest Files:")
print(run("find ~ -type f -exec du -h {} + | sort -hr | head -n 10"))

# 5. Daemon & Watchdog
print("\n📡 SYSTEM TRIGGERS")
status("rotor_trigger.txt", check_file("rotor_trigger.txt"))
status("watchdog.py", check_file("watchdog.py"))
status("status_check.py", check_file("status_check.py"))
status("governor.py", check_file("governor.py"))

# 6. Runtime Tools
print("\n🛠️ RUNTIME TOOLCHAIN")
status("Python3 Installed", check_command("python3"))
status("Node.js Installed", check_command("node"))
status("FPDF Installed", check_python_package("fpdf"))

print("\n✅ SYSTEM CHECK COMPLETE — REVIEW ABOVE FOR ANY RED FLAGS\n")
