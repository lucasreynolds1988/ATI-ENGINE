import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi import APIRouter, Header
from backend.utils.auth import validate_token
import os
import json

router = APIRouter()

@router.get("/manual/info/{manual_id}")
async def get_manual_info(manual_id: str, x_api_token: str = Header(...)):
    if not validate_token(x_api_token):
        return {"error": "Invalid token"}

    try:
        path = f"memory/manuals/{manual_id}.json"
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
        return {"error": "Manual not found"}
    except Exception as e:
        return {"error": str(e)}
