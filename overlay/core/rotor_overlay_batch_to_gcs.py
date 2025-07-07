import os
import subprocess

def batch_to_gcs():
    overlay = os.path.expanduser("~/Soap/overlay")
    for fname in os.listdir(overlay):
        fpath = os.path.join(overlay, fname)
        if os.path.isfile(fpath):
            subprocess.run(["gsutil", "cp", fpath, "gs://ati-oracle-engine/backups/"])
            print(f"Uploaded {fname} to GCS.")

if __name__ == "__main__":
    batch_to_gcs()
