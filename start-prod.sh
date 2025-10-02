#!/bin/bash

echo "🚀 Starting AI Knowledge Base in production mode..."

# Start FastAPI backend directly on Railway's port
cd /app
echo "🌐 Starting FastAPI on port $PORT..."
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
