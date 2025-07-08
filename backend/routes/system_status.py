import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi import APIRouter, Header
from backend.utils.auth import validate_token
import time

router = APIRouter()

@router.get("/status")
async def system_status(x_api_token: str = Header(...)):
    if not validate_token(x_api_token):
        return {"error": "Invalid token"}

    return {
        "heartbeat": True,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "rotors_active": True
    }
