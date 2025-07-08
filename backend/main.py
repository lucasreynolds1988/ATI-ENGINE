from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import uuid
from pymongo import MongoClient

# Core logic
from core.text_extract import extract_text
from core.chunking import chunk_text
from core.vectorizer import vectorize_all
from core.mongo_vectors import store_chunk
from core.rotor_chunk_and_stream import rotor_chunk_and_upload

# Route imports
from backend.routes.synthesize import router as synth_router
from backend.routes.upload_manual import router as upload_router
from backend.routes.chat import router as chat_router
from backend.routes.scrape_url import router as scrape_router
from backend.routes.roles import router as roles_router
from backend.routes.pipeline_status import router as status_router
from backend.routes.pipeline_history import router as history_router
from backend.routes.log import router as log_router
from backend.routes.config import router as config_router
from backend.routes.token_check import router as token_router
from backend.routes.upload_list import router as upload_list_router
from backend.routes.system_status import router as system_status_router
from backend.routes.heartbeat import router as heartbeat_router
from backend.routes.system_ping import router as ping_router
from backend.routes.manual_info import router as manual_info_router
from backend.routes.vector_search import router as vector_search_router
from backend.routes.sop_generate import router as sop_generate_router

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routes
app.include_router(synth_router)
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(scrape_router)
app.include_router(roles_router)
app.include_router(status_router)
app.include_router(history_router)
app.include_router(log_router)
app.include_router(config_router)
app.include_router(token_router)
app.include_router(upload_list_router)
app.include_router(system_status_router)
app.include_router(heartbeat_router)
app.include_router(ping_router)
app.include_router(manual_info_router)
app.include_router(vector_search_router)
app.include_router(sop_generate_router)

# Manual upload + chunking route
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

# MongoDB connection test route
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
