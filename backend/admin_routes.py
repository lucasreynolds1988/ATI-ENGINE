from fastapi import APIRouter, Query
from core.ai_admin import record_manual_metadata
from core.job_tracker import log_job, update_job_status
from pymongo import MongoClient

router = APIRouter()

@router.post("/admin/approve_manual")
def approve_manual(manual_id: str, approved: bool = True, notes: str = ""):
    record_manual_metadata(manual_id, filename="", uploader="", approved=approved, notes=notes)
    return {"status": "ok"}

@router.get("/admin/jobs")
def jobs(status: str = Query(None)):
    client = MongoClient()
    col = client["fusion"]["jobs"]
    query = {}
    if status:
        query["status"] = status
    return list(col.find(query, {"_id": 0}))
