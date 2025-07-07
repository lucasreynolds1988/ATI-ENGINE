#!/bin/bash
# Build React frontend, copy to backend, and start FastAPI (one port, one process!)

# Exit on error
set -e

# 1. Build React
echo "Building React frontend..."
cd ~/Soap/frontend
npm run build

# 2. Ensure static folder exists
echo "Ensuring backend static directory exists..."
mkdir -p ~/Soap/backend/static/

# 3. Copy built files to backend
echo "Copying build to backend/static..."
cp -r build/* ../backend/static/

# 4. Start FastAPI (kill previous if running)
echo "Launching FastAPI backend (serves all on port 5003)..."
cd ~/Soap/backend

# Kill previous uvicorn if running on 5003 (optional/safe)
if lsof -Pi :5003 -sTCP:LISTEN -t >/dev/null ; then
  echo "Killing previous FastAPI (port 5003)..."
  kill -9 $(lsof -Pi :5003 -sTCP:LISTEN -t)
  sleep 2
fi

# Activate venv (if not already)
source ~/Soap/backend/venv/bin/activate

# Run FastAPI
uvicorn main:app --host 0.0.0.0 --port 5003
