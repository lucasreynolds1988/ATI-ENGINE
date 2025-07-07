import os
import subprocess
import hashlib
import shutil

def backup_compress_upload_verify():
    overlay = os.path.expanduser("~/Soap/overlay")
    backup_dir = os.path.expanduser("~/Soap/overlay_backup")
    os.makedirs(backup_dir, exist_ok=True)
    # 1. Backup
    for fname in os.listdir(overlay):
        shutil.copy2(os.path.join(overlay, fname), backup_dir)
    print("Step 1: Backup complete.")
    # 2. Compress
    zip_path = os.path.expanduser("~/Soap/overlay_backup.zip")
    subprocess.run(["zip", "-r", zip_path, "."], cwd=backup_dir)
    print("Step 2: Compression complete.")
    # 3. Upload to GCS
    subprocess.run(["gsutil", "cp", zip_path, "gs://ati-oracle-engine/backups/"])
    print("Step 3: Upload complete.")
    # 4. Verify SHA256 with GCS
    def sha256sum(filename):
        h = hashlib.sha256()
        b = bytearray(128*1024)
        mv = memoryview(b)
        with open(filename, 'rb', buffering=0) as f:
            for n in iter(lambda : f.readinto(mv), 0):
                h.update(mv[:n])
        return h.hexdigest()
    local_sha = sha256sum(zip_path)
    gcs_tmp = "/tmp/overlay_backup.zip"
    subprocess.run(["gsutil", "cp", "gs://ati-oracle-engine/backups/overlay_backup.zip", gcs_tmp])
    gcs_sha = sha256sum(gcs_tmp) if os.path.exists(gcs_tmp) else "N/A"
    print("Step 4: SHA256 local:", local_sha)
    print("Step 4: SHA256 GCS:  ", gcs_sha)
    print("Step 5: Verification", "PASSED" if local_sha == gcs_sha else "FAILED")

if __name__ == "__main__":
    backup_compress_upload_verify()
