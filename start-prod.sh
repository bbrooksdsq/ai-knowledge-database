#!/bin/bash

echo "🚀 Starting AI Knowledge Base in production mode..."

# Start FastAPI backend in background on internal port 8000
cd /app
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Use envsubst to replace $PORT in nginx config template
envsubst '${PORT}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Start nginx (listens on $PORT externally, proxies to backend on 8000)
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
