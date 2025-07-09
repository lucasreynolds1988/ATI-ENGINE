# ~/Soap/core/cleanup_utils.py

import os
import shutil

BLOAT_EXTS = [".tmp", ".gstmp", ".part", ".part_aa", ".cache"]
BLOAT_DIRS = ["__pycache__", "venv", ".ipynb_checkpoints"]

def clear_bloat(base_path="/home/lucasreynolds1988"):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if any(file.endswith(ext) for ext in BLOAT_EXTS):
                try:
                    os.remove(os.path.join(root, file))
                except: pass
        for dir in dirs:
            if dir in BLOAT_DIRS:
                try:
                    shutil.rmtree(os.path.join(root, dir))
                except: pass
