import os
import shutil
from core.rotor_overlay import log_event

def cleanup_all():
    base = os.path.expanduser("~/Soap")
    to_clean = ["overlay", "logs", "vectorizer", "uploads"]
    for d in to_clean:
        path = os.path.join(base, d)
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
                log_event(f"rotor_cleanup_all: Removed directory {path}")
            else:
                os.remove(path)
                log_event(f"rotor_cleanup_all: Removed file {path}")
    log_event("rotor_cleanup_all: Cleanup completed.")

if __name__ == "__main__":
    cleanup_all()
