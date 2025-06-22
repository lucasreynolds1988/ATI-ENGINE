# ~/Soap/code_red.py

import os
import subprocess
import time
import glob
from relay_log_hook import run_viewer

def copy_token_if_needed():
    try:
        target = os.path.expanduser("~/.config/gcloud/application_default_credentials.json")
        if not os.path.exists(target):
            temp_paths = glob.glob("/tmp/tmp*/application_default_credentials.json")
            if temp_paths:
                os.makedirs(os.path.dirname(target), exist_ok=True)
                subprocess.run(["cp", temp_paths[0], target], check=True)
                print(f"🔐 Copied GCP token to ADC path")
            else:
                print("⚠️ No temp token found in /tmp/")
    except Exception as e:
        print(f"❌ Token setup failed: {e}")

def ensure_gcs_bucket_and_mount():
    mount_path = os.path.expanduser("~/Soap_overlay")
    bucket_name = "ati-rotor-fusion"

    if not os.path.ismount(mount_path):
        print("☁️ GCS overlay not mounted — attempting now...")
        try:
            subprocess.run(["gsutil", "ls", f"gs://{bucket_name}"], check=True)
        except subprocess.CalledProcessError:
            print("🛢️ GCS bucket missing — creating...")
            subprocess.run([
                "gsutil", "mb",
                "-p", "vivid-fragment-462823-r7",
                "-c", "STANDARD",
                "-l", "us-central1",
                f"gs://{bucket_name}"
            ], check=True)

        os.makedirs(mount_path, exist_ok=True)
        subprocess.run(["gcsfuse", bucket_name, mount_path], check=True)
        print(f"✅ GCS overlay mounted to {mount_path}")

def trigger_rotor_fusion():
    print("🧠 Launching +CODE-RED+ Rotor FUSION")
    subprocess.run(["python3", os.path.expanduser("~/Soap/rotor_fusion.py")], check=True)

def main():
    copy_token_if_needed()
    ensure_gcs_bucket_and_mount()
    trigger_rotor_fusion()
    print("📊 Reviewing last 5 relay log entries...")
    run_viewer("last")

if __name__ == "__main__":
    main()
