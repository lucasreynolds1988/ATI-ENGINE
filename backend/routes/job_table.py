from fastapi import APIRouter, Header
from backend.utils.auth import validate_token
from backend.utils.mongo import get_collection

router = APIRouter()

@router.get("/job-table")
async def get_jobs(x_api_token: str = Header(...)):
    if not validate_token(x_api_token):
        return {"error": "Invalid token"}
    
    collection = get_collection("jobs")
    jobs = list(collection.find({}, {"_id": 0}))
    return {"jobs": jobs}
