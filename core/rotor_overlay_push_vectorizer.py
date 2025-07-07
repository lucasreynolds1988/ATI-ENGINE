import os
import shutil

def push_to_vectorizer():
    overlay = os.path.expanduser("~/Soap/overlay")
    vector_dir = os.path.expanduser("~/Soap/vectorizer")
    os.makedirs(vector_dir, exist_ok=True)
    for fname in os.listdir(overlay):
        src = os.path.join(overlay, fname)
        dst = os.path.join(vector_dir, fname)
        if os.path.isfile(src):
            shutil.copy2(src, dst)
            print(f"Copied {fname} from overlay to vectorizer.")

if __name__ == "__main__":
    push_to_vectorizer()
