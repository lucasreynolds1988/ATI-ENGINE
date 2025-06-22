# ~/Soap/sop_chunk_mapper.py

import os
import json
from pathlib import Path

CHUNK_DIR = Path.home() / "Soap/chunks"
CHUNK_SIZE = 3000  # characters per chunk

def chunk_sop_file(sop_path):
    CHUNK_DIR.mkdir(parents=True, exist_ok=True)

    try:
        with open(sop_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading SOP file: {e}")
        return

    chunks = []
    for i in range(0, len(content), CHUNK_SIZE):
        chunk = content[i:i + CHUNK_SIZE]
        chunks.append({
            "chunk_id": i // CHUNK_SIZE,
            "text": chunk.strip()
        })

    chunk_file = CHUNK_DIR / f"{Path(sop_path).stem}_chunks.json"
    try:
        with open(chunk_file, "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=2)
        print(f"✅ Split into {len(chunks)} chunks → {chunk_file}")
    except Exception as e:
        print(f"❌ Failed to write chunk file: {e}")

    return {"chunk_count": len(chunks), "output": str(chunk_file)}

if __name__ == "__main__":
    test_path = input("📄 Enter SOP file path to chunk: ").strip()
    if os.path.exists(test_path) and test_path.endswith(".txt"):
        result = chunk_sop_file(test_path)
        if result:
            print(json.dumps(result, indent=2))
    else:
        print("❌ Invalid or missing .txt file.")
