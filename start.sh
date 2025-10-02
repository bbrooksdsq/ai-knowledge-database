#!/bin/bash

# AI Knowledge Base Startup Script

echo "🚀 Starting AI Knowledge Base..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your OpenAI API key!"
fi

# Create uploads directory
mkdir -p uploads

# Start services with Docker Compose
echo "🐳 Starting services with Docker Compose..."
docker-compose up --build

echo "✅ AI Knowledge Base is running!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
