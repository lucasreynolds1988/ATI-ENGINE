import os
import subprocess
import time
from core.rotor_overlay import log_event
from core.mongo_safe_upload_v2 import mongo_safe_upload
from core.cloud_stream_relay import stream_to_cloud

ESSENTIAL = os.path.expanduser("~/Soap/_file_inventory.txt")
GCS_BUCKET = "gs://ati-oracle-engine/backups/"

def save_to_github():
    try:
        subprocess.run(["git", "add", ESSENTIAL], check=True)
        subprocess.run(["git", "commit", "-m", "🔒 +SAVEALL: Updated essentials manifest"], check=True)
        subprocess.run(["git", "push"], check=True)
        log_event("+SAVEALL+: Pushed essentials to GitHub")
    except Exception as e:
        log_event(f"+SAVEALL+: GitHub push failed — {e}")

def save_to_mongo():
    try:
        mongo_safe_upload(ESSENTIAL)
    except Exception as e:
        log_event(f"+SAVEALL+: Mongo upload failed — {e}")

def save_to_gcs():
    try:
        zip_path = f"/tmp/ATI_FILE_INVENTORY_{int(time.time())}.zip"
        subprocess.run(["zip", "-j", zip_path, ESSENTIAL], check=True)
        subprocess.run(["gsutil", "cp", zip_path, GCS_BUCKET], check=True)
        log_event(f"+SAVEALL+: Uploaded zip to GCS: {zip_path}")
    except Exception as e:
        log_event(f"+SAVEALL+: GCS upload failed — {e}")

if __name__ == "__main__":
    save_to_github()
    save_to_mongo()
    save_to_gcs()
