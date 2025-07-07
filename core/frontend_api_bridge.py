#!/usr/bin/env python3
from fastapi import APIRouter, Request
from core.sop_generator import generate_sop

router = APIRouter()

@router.post("/frontend/ask_ai")
async def ask_ai(request: Request):
    data = await request.json()
    question = data.get("question", "")
    engine = data.get("engine", "openai")
    result = generate_sop(question, engine=engine)
    return {"answer": result}
