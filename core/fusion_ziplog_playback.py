# ~/Soap/core/fusion_ziplog_playback.py

import os
import zipfile
from core.rotor_overlay import log_event

def unzip_latest_backup(zip_path, target_dir):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(target_dir)
        log_event(f"[ZIPLOG] 🔓 Unzipped to: {target_dir}")
    except Exception as e:
        log_event(f"[ZIPLOG] ❌ Failed: {str(e)}")
