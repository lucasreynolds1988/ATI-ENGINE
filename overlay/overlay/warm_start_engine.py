# ~/Soap/warm_start_engine.py

import time
import subprocess
import os

BASE = os.path.expanduser("~/Soap/core")

def load_ontology():
    print("[🧠] Loading ontology...")
    subprocess.run(["python3", os.path.join(BASE, "ontology_loader.py")], check=True)

def restore_vector_memory():
    print("[🔗] Restoring vector memory...")
    subprocess.run(["python3", os.path.join(BASE, "vector_memory_restore.py")], check=True)

def load_manual_cache():
    print("[📘] Loading manual archive into memory...")
    subprocess.run(["python3", os.path.join(BASE, "manual_cache_loader.py")], check=True)

def warm_start_all():
    print("[🔥] Starting AI warm-start sequence...")
    load_ontology()
    restore_vector_memory()
    load_manual_cache()
    print("[✅] AI systems are warm and ready.")

if __name__ == "__main__":
    warm_start_all()
