import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi import APIRouter, Header
from fastapi.responses import FileResponse
from backend.utils.auth import validate_token
import os

router = APIRouter()

@router.get("/final/{file_id}")
async def fetch_final(file_id: str, x_api_token: str = Header(...)):
    if not validate_token(x_api_token):
        return {"error": "Invalid token"}

    final_path = f"./upload/{file_id}.final.txt"
    if os.path.exists(final_path):
        return FileResponse(final_path, media_type="text/plain", filename=f"{file_id}.final.txt")
    return {"error": f"{file_id}.final.txt not found"}
