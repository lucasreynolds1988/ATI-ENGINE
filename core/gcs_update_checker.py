import subprocess
import re

def latest_gcs_zip():
    cmd = "gsutil ls -l gs://ati-oracle-engine/backups/"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    lines = result.stdout.splitlines()
    zips = [l for l in lines if l.endswith(".zip")]
    if not zips:
        return None
    latest = sorted(zips)[-1].split()[-1]
    return latest

def needs_update(current_version_file, gcs_uri):
    try:
        current = open(current_version_file).read().strip()
        return current not in gcs_uri
    except:
        return True
