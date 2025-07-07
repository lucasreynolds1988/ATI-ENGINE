import gzip
import shutil
import os

def compress_log(log_path):
    if not os.path.exists(log_path):
        return None
    compressed_path = log_path + ".gz"
    with open(log_path, "rb") as f_in:
        with gzip.open(compressed_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    return compressed_path
