#!/bin/bash

echo "🚀 Starting AI Knowledge Base in production mode..."

# Start FastAPI backend in background on internal port 8000
cd /app
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 10

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Backend failed to start"
    exit 1
fi

echo "✅ Backend started successfully"

# Check if static files exist
echo "📁 Checking static files..."
if [ -f "/app/static/index.html" ]; then
    echo "✅ Static files found:"
    ls -la /app/static/
else
    echo "❌ Static files not found!"
    echo "Contents of /app/static/:"
    ls -la /app/static/ || echo "Directory does not exist"
fi

# Use envsubst to replace $PORT in nginx config template
echo "🔧 Configuring nginx..."
envsubst '${PORT}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Test nginx config
nginx -t
if [ $? -ne 0 ]; then
    echo "❌ Nginx config test failed"
    cat /etc/nginx/nginx.conf
    exit 1
fi

echo "✅ Nginx config is valid"

# Start nginx (listens on $PORT externally, proxies to backend on 8000)
echo "🌐 Starting nginx..."
nginx -g "daemon off;" &
NGINX_PID=$!

# Wait a moment and check if nginx started
sleep 2
if ! kill -0 $NGINX_PID 2>/dev/null; then
    echo "❌ Nginx failed to start"
    exit 1
fi

echo "✅ Nginx started successfully"
echo "🚀 Application is ready!"

# Function to handle shutdown
cleanup() {
    echo "🛑 Shutting down services..."
    kill $BACKEND_PID $NGINX_PID 2>/dev/null
    exit 0
}

# Trap shutdown signals
trap cleanup SIGTERM SIGINT

# Wait for processes
wait
