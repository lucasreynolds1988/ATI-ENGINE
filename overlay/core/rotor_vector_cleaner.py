import os
from core.rotor_overlay import log_event

def clean_vectors():
    vector_dir = os.path.expanduser("~/Soap/vectorizer")
    for f in os.listdir(vector_dir):
        if f.endswith(".vec") or f.endswith(".tmp"):
            os.remove(os.path.join(vector_dir, f))
            log_event(f"rotor_vector_cleaner: Removed {f}")

if __name__ == "__main__":
    clean_vectors()
