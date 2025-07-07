import os
import subprocess

def batch_from_gcs():
    overlay = os.path.expanduser("~/Soap/overlay")
    subprocess.run(["gsutil", "cp", "gs://ati-oracle-engine/backups/*", overlay])
    print("Downloaded all files from GCS to overlay.")

if __name__ == "__main__":
    batch_from_gcs()
