#!/bin/bash

echo "🗄️  Initializing AI Knowledge Base Database..."

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
until docker-compose exec -T postgres pg_isready -U user -d knowledge_base; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "✅ PostgreSQL is ready!"

# Initialize Alembic and create initial migration
echo "📝 Setting up database migrations..."
cd backend

# Initialize alembic if not already done
if [ ! -d "alembic/versions" ] || [ -z "$(ls -A alembic/versions)" ]; then
    echo "Creating initial migration..."
    alembic revision --autogenerate -m "Initial migration"
fi

# Run migrations
echo "🔄 Running database migrations..."
alembic upgrade head

echo "✅ Database initialized successfully!"
echo "🚀 You can now start the application with: ./start.sh"
