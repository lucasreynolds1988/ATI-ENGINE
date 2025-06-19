# ~/Soap/compressor_zstd.py

import os
import tarfile
import zstandard as zstd

def compress_zstd(source_dir, output_path):
    with open(output_path, "wb") as f_out:
        cctx = zstd.ZstdCompressor(level=10)
        with cctx.stream_writer(f_out) as compressor:
            with tarfile.open(fileobj=compressor, mode="w|") as tar:
                tar.add(source_dir, arcname=os.path.basename(source_dir))
    return output_path
