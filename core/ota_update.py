import os
import zipfile
import requests

def apply_zip(zip_url, extract_to="./", auth=None):
    print(f"Downloading OTA zip: {zip_url}")
    r = requests.get(zip_url, stream=True, headers=auth or {})
    if r.status_code != 200:
        print("Failed to download zip.")
        return False

    tmp_path = "/tmp/ota_patch.zip"
    with open(tmp_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    print("Extracting zip...")
    with zipfile.ZipFile(tmp_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
    os.remove(tmp_path)
    return True
