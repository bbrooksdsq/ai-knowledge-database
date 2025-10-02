#!/bin/bash

echo "🚀 Starting AI Knowledge Base in production mode..."

# Start FastAPI backend in background
cd /app
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start nginx
nginx -g "daemon off;" &
NGINX_PID=$!

# Function to handle shutdown
cleanup() {
    echo "🛑 Shutting down services..."
    kill $BACKEND_PID $NGINX_PID
    exit 0
}

# Trap shutdown signals
trap cleanup SIGTERM SIGINT

# Wait for processes
wait
