from fastapi import APIRouter, Header
from backend.utils.auth import validate_token
from backend.utils.mongo import get_collection

router = APIRouter()

@router.post("/pipeline/run/{file_id}")
async def run_pipeline(file_id: str, x_api_token: str = Header(...)):
    if not validate_token(x_api_token):
        return {"error": "Invalid token"}
    
    # Simulate starting a pipeline process
    collection = get_collection("pipeline_status")
    collection.update_one(
        {"file_id": file_id},
        {"$set": {"status": "running"}},
        upsert=True
    )

    # Log to pipeline history
    history = get_collection("pipeline_history")
    history.insert_one({"file_id": file_id, "event": "Pipeline started"})

    return {"message": f"Pipeline run triggered for {file_id}"}
