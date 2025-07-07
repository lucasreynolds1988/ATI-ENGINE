import os
import time
from pathlib import Path
from Soap.core.rotor_overlay import log_event

def upload_chunks(directory, chunk_size_mb=13):
    upload_dir = Path(directory)
    if not upload_dir.exists():
        log_event("Upload directory missing.", "ERROR")
        return

    for file in upload_dir.glob("*"):
        size_mb = file.stat().st_size / (1024 * 1024)
        if size_mb > chunk_size_mb:
            log_event(f"{file.name} too big ({size_mb:.2f}MB). Splitting...", "WARNING")
            # Placeholder for actual splitting logic
        else:
            log_event(f"{file.name} ready for MongoDB upload.", "INFO")
            time.sleep(2)  # Simulate pacing

if __name__ == "__main__":
    upload_chunks(str(Path.home() / "Soap/uploads"))
