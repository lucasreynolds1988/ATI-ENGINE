#!/usr/bin/env python3
import os
import subprocess

REPO_URL = "https://github.com/lucasr610/Soap.git"
CLONE_DIR = os.path.expanduser("~/Soap")

def clone_or_pull():
    if not os.path.exists(os.path.join(CLONE_DIR, ".git")):
        print(f"Cloning repo to {CLONE_DIR}")
        subprocess.run(["git", "clone", REPO_URL, CLONE_DIR], check=True)
    else:
        print(f"Repo exists, pulling latest in {CLONE_DIR}")
        subprocess.run(["git", "-C", CLONE_DIR, "pull"], check=True)

if __name__ == "__main__":
    clone_or_pull()
