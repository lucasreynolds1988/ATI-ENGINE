from fastapi import APIRouter, Request, Header
from backend.utils.auth import validate_token
from core.vectorizer import get_openai_vector, get_gemini_vector, get_ollama_vector
from core.mongo_vectors import find_similar

router = APIRouter()

@router.post("/vector/search/{engine}")
async def vector_search(engine: str, request: Request, x_api_token: str = Header(...)):
    if not validate_token(x_api_token):
        return {"error": "Invalid token"}

    data = await request.json()
    query = data.get("query")
    if not query:
        return {"error": "Missing query"}

    if engine == "openai":
        vector = get_openai_vector(query)
    elif engine == "gemini":
        vector = get_gemini_vector(query)
    elif engine == "ollama":
        vector = get_ollama_vector(query)
    else:
        return {"error": "Invalid engine"}

    results = find_similar(engine, vector)
    return {"results": results}
