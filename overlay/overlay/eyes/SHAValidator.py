#!/usr/bin/env python3
import hashlib
from core.rotor_overlay import log_event

def validate_sha(file_path, expected_sha):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    calculated_sha = sha256_hash.hexdigest()
    is_valid = calculated_sha == expected_sha
    log_event("SHA_VALIDATOR", f"{file_path}: Expected {expected_sha}, Calculated {calculated_sha}, Valid: {is_valid}")
    return is_valid
