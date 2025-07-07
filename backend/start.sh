#!/bin/bash
echo "[START] Starting FastAPI server..."
uvicorn backend.main:app --host 0.0.0.0 --port 3000 --reload
