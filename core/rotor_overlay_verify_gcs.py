import os
import subprocess
import hashlib

def sha256sum(filename):
    h = hashlib.sha256()
    b = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()

def verify_gcs(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    local_path = os.path.join(overlay, filename)
    gcs_path = f"gs://ati-oracle-engine/backups/{filename}"
    tmpfile = f"/tmp/{filename}.gcs"
    subprocess.run(["gsutil", "cp", gcs_path, tmpfile], check=False)
    if not os.path.isfile(tmpfile):
        print(f"{filename} not found in GCS bucket.")
        return
    local_sha = sha256sum(local_path)
    gcs_sha = sha256sum(tmpfile)
    if local_sha == gcs_sha:
        print(f"SHA256 match for {filename} (local & GCS): {local_sha}")
    else:
        print(f"SHA256 MISMATCH!\nLocal: {local_sha}\nGCS:   {gcs_sha}")
    os.remove(tmpfile)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        verify_gcs(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_verify_gcs.py <filename>")
