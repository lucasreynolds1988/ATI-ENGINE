import os
from google.cloud import storage

BUCKET_NAME = "ati-rotor-bucket"
UPLOAD_DIR = "/tmp"

def upload_to_gcs():
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)

    for filename in os.listdir(UPLOAD_DIR):
        if filename.endswith(".tar.gz"):
            local_path = os.path.join(UPLOAD_DIR, filename)
            blob = bucket.blob(filename)
            blob.upload_from_filename(local_path)
            print(f"☁️ Uploaded to GCS: {filename}")
            os.remove(local_path)

if __name__ == "__main__":
    upload_to_gcs()
