# ~/Soap/cloud_saver_pip.py

import os
import zipfile
import requests
from pathlib import Path
from google.cloud import storage  # Requires `google-cloud-storage`

# CONFIGURATION
PACKAGE_NAME = "pymongo"
PACKAGE_VERSION = "4.6.3"
GCS_BUCKET = "your-gcs-bucket-name"
EXTRACT_DIR = "/tmp/cloud_pip_extract"

def download_package():
    url = f"https://files.pythonhosted.org/packages/py3/{PACKAGE_NAME[0]}/{PACKAGE_NAME}/{PACKAGE_NAME}-{PACKAGE_VERSION}-py3-none-any.whl"
    local_whl = f"/tmp/{PACKAGE_NAME}.whl"

    print(f"⬇️ Downloading {url}")
    response = requests.get(url)
    response.raise_for_status()
    
    with open(local_whl, "wb") as f:
        f.write(response.content)
    
    print(f"✅ Downloaded to {local_whl}")
    return local_whl

def upload_to_gcs(local_path, rel_path, bucket_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(f"{PACKAGE_NAME}/{rel_path}")
    
    blob.upload_from_filename(local_path)
    print(f"☁️ Uploaded: {rel_path}")
    
    os.remove(local_path)
    print(f"🧹 Deleted local: {rel_path}")

def extract_and_offload(whl_path):
    Path(EXTRACT_DIR).mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(whl_path, 'r') as z:
        for member in z.namelist():
            extracted_path = os.path.join(EXTRACT_DIR, member)
            z.extract(member, path=EXTRACT_DIR)

            if os.path.isfile(extracted_path):
                upload_to_gcs(extracted_path, member, GCS_BUCKET)

    print("✅ All files extracted and uploaded.")

def main():
    whl_path = download_package()
    extract_and_offload(whl_path)
    os.remove(whl_path)
    print("🏁 Finished cloud-save process.")

if __name__ == "__main__":
    main()
