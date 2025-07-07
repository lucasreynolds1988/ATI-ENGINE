from fastapi import APIRouter, Header
from backend.utils.auth import validate_token
import os

router = APIRouter()

@router.get("/upload/list")
async def list_uploads(x_api_token: str = Header(...)):
    if not validate_token(x_api_token):
        return {"error": "Invalid token"}

    files = os.listdir("uploads") if os.path.exists("uploads") else []
    return {"files": files}
