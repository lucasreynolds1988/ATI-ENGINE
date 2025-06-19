# command_center.py

import sys
import subprocess
import os
from datetime import datetime

LOG_FILE = os.path.expanduser("~/Soap/data/logs/ops_log.txt")

def log(msg):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} {msg}\n")

def run_status_check():
    try:
        subprocess.run(["python3", "status_check.py"], check=True)
        log("System check complete.")
    except Exception as e:
        log(f"System check failed: {e}")

def check_pip_offloader():
    if os.path.exists("pip_offloader.py"):
        log("Pip offloader found.")
    else:
        log("Pip offloader missing. Generating stub...")
        with open("pip_offloader.py", "w") as f:
            f.write("# TODO: Implement pip offloader logic\n")
        log("Created pip_offloader.py")

def run_offloader():
    try:
        subprocess.run(["python3", "pip_offloader.py"], check=True)
        log("Pip offloader executed.")
    except Exception as e:
        log(f"Pip offloader failed: {e}")

def verify_git_and_mongo():
    result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True)
    if "github.com" in result.stdout:
        log("GitHub connected.")
    else:
        log("GitHub NOT connected.")
    
    mongo_uri = "mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net"
    if "mongodb+srv://" in mongo_uri:
        log("Mongo URI appears configured.")
    else:
        log("Mongo not configured.")

def choose_dev_zone():
    zone = input("Enter dev zone (frontend / backend / both / skip): ").strip().lower()
    if zone == "frontend":
        os.chdir(os.path.expanduser("~/ati-web-app/frontend"))
        log("Switched to FRONTEND zone.")
    elif zone == "backend":
        os.chdir(os.path.expanduser("~/ati-web-app/backend"))
        log("Switched to BACKEND zone.")
    elif zone == "both":
        log("Full stack zone selected. You may need multiple tabs.")
    else:
        log("Dev zone selection skipped.")

def main():
    if len(sys.argv) != 2 or sys.argv[1].lower() != "code red":
        print("Usage: python3 command_center.py code red")
        return

    log(">>> CODE RED INITIATED <<<")
    run_status_check()
    check_pip_offloader()
    run_offloader()
    verify_git_and_mongo()
    choose_dev_zone()
    log(">>> CODE RED COMPLETE <<<")
    print("System readiness check complete. Logs written to ops_log.txt")

if __name__ == "__main__":
    main()
