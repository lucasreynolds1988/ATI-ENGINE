import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi import APIRouter, Header
from backend.utils.auth import validate_token

router = APIRouter()

@router.get("/check-token")
async def check_token(x_api_token: str = Header(...)):
    if not validate_token(x_api_token):
        return {"valid": False}
    return {"valid": True}
