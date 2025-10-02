# AI Knowledge Base - Setup Guide

## Quick Start

1. **Clone and Setup**
   ```bash
   git clone <your-repo>
   cd ai-knowledge-base
   cp .env.example .env
   ```

2. **Add OpenAI API Key**
   Edit `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   ```

3. **Start the Application**
   ```bash
   ./start.sh
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Features Implemented

### ✅ Core Infrastructure
- **Backend**: FastAPI with PostgreSQL and Redis
- **Frontend**: Next.js 14 with Tailwind CSS
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Vector Search**: Semantic search with embeddings
- **AI Integration**: OpenAI API for embeddings and processing

### ✅ Search Capabilities
- **Semantic Search**: Natural language queries using vector embeddings
- **Keyword Search**: Traditional text-based search
- **Real-time Results**: Fast search with execution time tracking
- **Search History**: Track and analyze search queries

### ✅ Document Management
- **File Upload**: Drag-and-drop interface for multiple file types
- **Auto-processing**: Automatic AI processing of uploaded documents
- **Metadata Extraction**: AI-generated tags, entities, and summaries
- **Document Viewer**: In-app viewing of all content types

### ✅ AI Features
- **Embedding Generation**: Automatic vector embeddings for semantic search
- **Content Summarization**: AI-generated summaries of documents
- **Tag Extraction**: Automatic tagging of content
- **Entity Recognition**: Extract people, dates, projects, topics

### ✅ User Interface
- **Modern Design**: Clean, responsive interface
- **Search Dashboard**: Google-like search experience
- **Upload Interface**: Intuitive file upload with progress tracking
- **Recent Documents**: View and manage recent additions

## Technical Architecture

### Backend Stack
- **Framework**: FastAPI
- **Database**: PostgreSQL with pgvector extension
- **Cache**: Redis
- **AI/ML**: OpenAI API, sentence-transformers
- **File Storage**: Local filesystem (easily upgradeable to S3)

### Frontend Stack
- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS with shadcn/ui components
- **State Management**: React hooks
- **HTTP Client**: Fetch API with error handling

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database Migrations**: Alembic
- **Development**: Hot reload for both frontend and backend

## API Endpoints

### Documents
- `POST /api/v1/documents/` - Upload new document
- `GET /api/v1/documents/` - List documents
- `GET /api/v1/documents/{id}` - Get specific document
- `PUT /api/v1/documents/{id}` - Update document
- `DELETE /api/v1/documents/{id}` - Delete document

### Search
- `POST /api/v1/documents/search` - Semantic search
- `POST /api/v1/documents/search/keyword` - Keyword search
- `GET /api/v1/documents/{id}/related` - Get related documents

## File Types Supported

- **Documents**: PDF, DOC, DOCX, TXT
- **Audio**: MP3, WAV, M4A (with transcription)
- **Video**: MP4, AVI, MOV
- **Maximum Size**: 50MB per file

## Development

### Running Individual Services

**Backend Only:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend Only:**
```bash
cd frontend
npm install
npm run dev
```

**Database Setup:**
```bash
# Start PostgreSQL and Redis
docker-compose up postgres redis

# Run migrations
cd backend
alembic upgrade head
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Required for AI features
OPENAI_API_KEY=your_openai_api_key_here

# Database (default works with Docker)
DATABASE_URL=postgresql://user:password@localhost:5432/knowledge_base

# Redis (default works with Docker)
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-change-in-production
```

## Production Deployment

### Docker Production Build
```bash
# Build production images
docker-compose -f docker-compose.prod.yml up --build
```

### Environment Considerations
- Use environment-specific `.env` files
- Set up proper SSL certificates
- Configure production database with connection pooling
- Set up file storage (S3, GCS, etc.)
- Configure monitoring and logging

## Troubleshooting

### Common Issues

1. **OpenAI API Errors**
   - Ensure API key is valid and has credits
   - Check rate limits
   - Verify API key is set in `.env`

2. **Database Connection Issues**
   - Ensure PostgreSQL is running
   - Check connection string in `.env`
   - Verify database exists

3. **File Upload Issues**
   - Check file size limits (50MB default)
   - Ensure uploads directory is writable
   - Verify file type is supported

4. **Search Not Working**
   - Ensure documents have been processed
   - Check if embeddings were generated
   - Verify OpenAI API key is working

### Logs
```bash
# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

## Next Steps

### Planned Enhancements
- [ ] User authentication and authorization
- [ ] Team collaboration features
- [ ] Advanced filtering and faceted search
- [ ] Integration with external platforms (Slack, Teams, etc.)
- [ ] Real-time notifications
- [ ] Analytics and usage tracking
- [ ] Mobile app
- [ ] API rate limiting and caching
- [ ] Advanced AI features (question answering, etc.)

### Integration Opportunities
- **Meeting Platforms**: Zoom, Google Meet, Teams
- **Communication**: Slack, Discord, Microsoft Teams
- **File Storage**: Google Drive, Dropbox, OneDrive
- **CRM Systems**: Salesforce, HubSpot
- **Project Management**: Jira, Asana, Trello

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Check logs for error details
4. Create an issue in the repository

---

**Built with ❤️ using FastAPI, Next.js, and OpenAI**
