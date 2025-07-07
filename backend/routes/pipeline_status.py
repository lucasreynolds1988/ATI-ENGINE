from fastapi import APIRouter, Header
from backend.utils.auth import validate_token
from backend.utils.mongo import get_collection

router = APIRouter()

@router.get("/pipeline/status/{file_id}")
async def get_pipeline_status(file_id: str, x_api_token: str = Header(...)):
    if not validate_token(x_api_token):
        return {"error": "Invalid token"}
    
    collection = get_collection("pipeline_status")
    record = collection.find_one({"file_id": file_id}, {"_id": 0})
    return {"status": record if record else "Not Found"}
