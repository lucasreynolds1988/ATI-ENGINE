from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
from core.text_extract import extract_text
from core.chunking import chunk_text
from core.vectorizer import vectorize_all, get_openai_vector, get_gemini_vector, get_ollama_vector
from core.mongo_vectors import store_chunk, find_similar
from core.rotor_chunk_and_stream import rotor_chunk_and_upload
from pymongo import MongoClient

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/manuals/upload")
async def upload_manual(file: UploadFile = File(...)):
    temp_path = f"/tmp/{uuid.uuid4()}_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    if os.path.getsize(temp_path) > 100 * 1024 * 1024:
        rotor_chunk_and_upload(temp_path)
        return {
            "status": "chunked",
            "note": "Large file sent to rotor chunker.",
            "filename": file.filename
        }

    try:
        text = extract_text(temp_path)
        chunks = chunk_text(text)
        manual_id = str(uuid.uuid4())
        for idx, chunk in enumerate(chunks):
            vectors = vectorize_all(chunk)
            store_chunk(manual_id, idx, chunk, vectors)
        os.remove(temp_path)
        return {"status": "ok", "manual_id": manual_id, "chunks": len(chunks)}
    except Exception as e:
        os.remove(temp_path)
        return {"status": "error", "error": str(e)}

@app.get("/mongo/test")
def mongo_test():
    try:
        uri = os.getenv("MONGO_URI", "mongodb+srv://lucasreynolds1988:Service%23%232244@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev")
        client = MongoClient(uri)
        db = client["fusion"]
        db["test"].insert_one({"ping": "pong"})
        return {"status": "ok", "message": "MongoDB connection succeeded"}
    except Exception as e:
        return {"status": "fail", "error": str(e)}
