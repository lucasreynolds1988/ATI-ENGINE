# ~/Soap/backend/routes/upload.py

from fastapi import APIRouter, UploadFile, File
from core.text_extract import extract_text
from core.chunking import chunk_text
from core.vectorizer import vectorize_all
from core.mongo_vectors import store_chunk
import uuid, os

router = APIRouter()

@router.post("/upload/manual")
async def upload_manual(file: UploadFile = File(...)):
    temp_path = f"/tmp/{uuid.uuid4()}_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    text = extract_text(temp_path)
    chunks = chunk_text(text)
    manual_id = str(uuid.uuid4())

    for i, chunk in enumerate(chunks):
        vectors = vectorize_all(chunk)
        store_chunk(manual_id, i, chunk, vectors)

    os.remove(temp_path)
    return {"manual_id": manual_id, "chunks": len(chunks)}
