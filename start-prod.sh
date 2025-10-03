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
echo "🔍 Testing if port $PORT is accessible..."
python -c "
import socket
import sys
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', int('$PORT')))
    sock.listen(1)
    print('✅ Port $PORT is available')
    sock.close()
except Exception as e:
    print(f'❌ Port $PORT error: {e}')
    sys.exit(1)
"
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
