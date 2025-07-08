import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi import APIRouter, Header
from backend.utils.auth import validate_token
from backend.utils.mongo import get_collection

router = APIRouter()

@router.get("/scavenger/status")
async def scavenger_status(x_api_token: str = Header(...)):
    if not validate_token(x_api_token):
        return {"error": "Invalid token"}
    
    collection = get_collection("scavenger_status")
    latest = collection.find_one(sort=[("_id", -1)], projection={"_id": 0})
    return {"scavenger": latest or {"status": "idle"}}
