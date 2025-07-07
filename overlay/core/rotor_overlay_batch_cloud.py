import os
import subprocess
from pymongo import MongoClient

GCS_BUCKET = "gs://ati-oracle-engine/backups/"
MONGO_URI = "mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev"

def upload_gcs():
    overlay = os.path.expanduser("~/Soap/overlay")
    for fname in os.listdir(overlay):
        fpath = os.path.join(overlay, fname)
        if os.path.isfile(fpath):
            subprocess.run(["gsutil", "cp", fpath, GCS_BUCKET], check=True)
            print(f"Uploaded {fname} to GCS.")

def download_gcs():
    overlay = os.path.expanduser("~/Soap/overlay")
    subprocess.run(["gsutil", "cp", f"{GCS_BUCKET}*", overlay])

def upload_mongo():
    from core.mongo_safe_upload_v2 import mongo_safe_upload
    overlay = os.path.expanduser("~/Soap/overlay")
    for fname in os.listdir(overlay):
        fpath = os.path.join(overlay, fname)
        if os.path.isfile(fpath):
            mongo_safe_upload(fpath)
            print(f"Uploaded {fname} to MongoDB.")

def download_mongo():
    client = MongoClient(MONGO_URI)
    db = client['fusion']
    col = db['files']
    overlay = os.path.expanduser("~/Soap/overlay")
    for doc in col.find():
        fname = doc["filename"]
        with open(os.path.join(overlay, fname), "wb") as f:
            f.write(doc["data"])
        print(f"Downloaded {fname} from MongoDB.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "upload_gcs":
            upload_gcs()
        elif mode == "download_gcs":
            download_gcs()
        elif mode == "upload_mongo":
            upload_mongo()
        elif mode == "download_mongo":
            download_mongo()
        else:
            print("Modes: upload_gcs | download_gcs | upload_mongo | download_mongo")
    else:
        print("Usage: python rotor_overlay_batch_cloud.py <mode>")
