from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
from core.text_extract import extract_text
from core.chunking import chunk_text
from core.vectorizer import vectorize_all, get_openai_vector, get_gemini_vector, get_ollama_vector
from core.mongo_vectors import store_chunk, find_similar

app = FastAPI()

# Enable CORS for local/frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in prod!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/manuals/upload")
async def upload_manual(file: UploadFile = File(...)):
    # Save file temporarily
    temp_path = f"/tmp/{uuid.uuid4()}_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    try:
        # Extract text and chunk
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

@app.post("/ai/query")
async def ai_query(
    question: str = Form(...), 
    engine: str = Form("openai"),
    top_k: int = Form(5)
):
    # Choose the vectorizer function
    vector_func = {
        "openai": get_openai_vector,
        "gemini": get_gemini_vector,
        "ollama": get_ollama_vector
    }[engine]
    q_vec = vector_func(question)
    results = find_similar(engine, q_vec, top_k=top_k)
    # Return best matches
    return {
        "matches": [
            {
                "text": doc["text"],
                "manual_id": doc["manual_id"],
                "chunk_index": doc["chunk_index"]
            }
            for doc in results
        ]
    }

@app.get("/health")
def health():
    return {"status": "ok"}
