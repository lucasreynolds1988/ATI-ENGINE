#!/bin/bash
# Start both backend (with reload) and frontend (with hot reload) in one go

# Make sure Python venv is activated
source ~/Soap/backend/venv/bin/activate

concurrently \
  "cd ~/Soap/backend && uvicorn main:app --reload --host 0.0.0.0 --port 5003" \
  "cd ~/Soap/frontend && npm start"
