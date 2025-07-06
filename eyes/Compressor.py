#!/usr/bin/env python3
import gzip
import shutil
from core.rotor_overlay import log_event

def compress_file(file_path):
    with open(file_path, 'rb') as f_in, gzip.open(file_path + '.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    log_event("COMPRESSOR", f"File compressed successfully: {file_path}.gz")
