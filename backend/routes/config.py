import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi import APIRouter, Header
from backend.utils.auth import validate_token

router = APIRouter()

@router.get("/config")
async def get_config(x_api_token: str = Header(...)):
    if not validate_token(x_api_token):
        return {"error": "Invalid token"}

    return {
        "version": "1.0.0",
        "engine": "ATI Oracle Engine",
        "mode": "operational",
        "backend": "FastAPI",
    }
