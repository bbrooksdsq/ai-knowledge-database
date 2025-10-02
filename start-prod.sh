#!/bin/bash

echo "🚀 Starting AI Knowledge Base in production mode..."

# Check if static files exist
echo "📁 Checking static files..."
if [ -f "/app/static/index.html" ]; then
    echo "✅ Static files found:"
    ls -la /app/static/
else
    echo "❌ Static files not found!"
    echo "Contents of /app/:"
    ls -la /app/
    echo "Contents of /app/static/:"
    ls -la /app/static/ || echo "Directory does not exist"
fi

# Start FastAPI backend directly on Railway's port
cd /app
echo "🌐 Starting FastAPI on port $PORT..."
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
