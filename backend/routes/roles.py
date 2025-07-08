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

@router.get("/roles")
async def get_roles(x_api_token: str = Header(...)):
    if not validate_token(x_api_token):
        return {"error": "Invalid token"}

    collection = get_collection("roles")
    roles = list(collection.find({}, {"_id": 0}))
    return {"roles": roles}
