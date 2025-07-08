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

@router.post("/sop/admin-review")
async def trigger_admin_review(x_api_token: str = Header(...)):
    if not validate_token(x_api_token):
        return {"error": "Invalid token"}

    review_queue = get_collection("admin_review_queue")
    review_queue.insert_one({"status": "pending", "message": "Manual review requested"})

    return {"message": "SOP review has been queued for admin."}
