# AI Team Knowledge Base

A centralized AI-powered knowledge management system that automatically ingests, processes, and makes searchable all team interactions including call transcripts, forms, documents, and other communications.

![AI Knowledge Base](https://img.shields.io/badge/AI-Powered-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)
![Next.js](https://img.shields.io/badge/Frontend-Next.js-black)
![OpenAI](https://img.shields.io/badge/AI-OpenAI-orange)

## 🚀 Quick Start

```bash
# Clone the repository
git clone <your-repo-url>
cd ai-knowledge-base

# Set up environment
cp .env.example .env
# Edit .env and add your OpenAI API key

# Start the application
./start.sh
```

**Access the application:**
- 🌐 Frontend: http://localhost:3000
- 🔧 Backend API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

## ✨ Features

### 🔍 **Intelligent Search**
- **Semantic Search**: Natural language queries that understand context and meaning
- **Keyword Search**: Traditional text-based search with filters
- **Real-time Results**: Fast search with execution time tracking
- **Related Documents**: AI-suggested related content

### 📁 **Document Management**
- **Multi-format Support**: PDFs, documents, audio, video files
- **Drag & Drop Upload**: Intuitive file upload interface
- **Auto-processing**: AI extracts content, generates summaries, and creates tags
- **Metadata Extraction**: Automatic entity recognition (people, dates, projects)

### 🤖 **AI-Powered Processing**
- **Vector Embeddings**: Semantic search using OpenAI embeddings
- **Content Summarization**: AI-generated summaries of documents
- **Smart Tagging**: Automatic categorization and tagging
- **Entity Recognition**: Extract people, dates, projects, topics

### 🎨 **Modern Interface**
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Clean UI**: Modern design with Tailwind CSS
- **Real-time Updates**: Live progress tracking and status updates
- **Intuitive Navigation**: Easy-to-use search and upload interfaces

## 🏗️ Architecture

### Backend Stack
- **FastAPI**: Modern, fast web framework for building APIs
- **PostgreSQL**: Robust relational database with vector support
- **Redis**: In-memory data store for caching
- **OpenAI API**: AI embeddings and content processing
- **Docker**: Containerized deployment

### Frontend Stack
- **Next.js 14**: React framework with App Router
- **Tailwind CSS**: Utility-first CSS framework
- **TypeScript**: Type-safe JavaScript
- **Responsive Design**: Mobile-first approach

## 📊 Project Structure

```
ai-knowledge-base/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── schemas/        # Pydantic schemas
│   ├── alembic/            # Database migrations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # App router pages
│   │   ├── components/    # React components
│   │   ├── lib/          # Utilities
│   │   └── styles/       # Global styles
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml      # Development environment
├── start.sh               # Quick start script
└── SETUP.md              # Detailed setup guide
```

## 🔧 API Endpoints

### Documents
- `POST /api/v1/documents/` - Upload new document
- `GET /api/v1/documents/` - List documents with pagination
- `GET /api/v1/documents/{id}` - Get specific document
- `PUT /api/v1/documents/{id}` - Update document
- `DELETE /api/v1/documents/{id}` - Delete document

### Search
- `POST /api/v1/documents/search` - Semantic search
- `POST /api/v1/documents/search/keyword` - Keyword search
- `GET /api/v1/documents/{id}/related` - Get related documents

## 📋 Supported File Types

- **Documents**: PDF, DOC, DOCX, TXT
- **Audio**: MP3, WAV, M4A (with transcription)
- **Video**: MP4, AVI, MOV
- **Maximum Size**: 50MB per file

## 🛠️ Development

### Prerequisites
- Docker and Docker Compose
- OpenAI API key (for AI features)
- Git

### Local Development

```bash
# Start all services
./start.sh

# Or start individually:
docker-compose up postgres redis    # Database services
cd backend && uvicorn app.main:app --reload  # Backend only
cd frontend && npm run dev          # Frontend only
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

## 🚀 Deployment

### Production with Docker

```bash
# Build and start production services
docker-compose -f docker-compose.prod.yml up --build
```

### Environment Setup
- Use environment-specific `.env` files
- Set up SSL certificates
- Configure production database with connection pooling
- Set up file storage (S3, GCS, etc.)
- Configure monitoring and logging

## 🔮 Roadmap

### Planned Features
- [ ] User authentication and authorization
- [ ] Team collaboration and sharing
- [ ] Integration with meeting platforms (Zoom, Teams)
- [ ] Slack/Discord integration
- [ ] Advanced analytics and insights
- [ ] Mobile application
- [ ] Real-time notifications
- [ ] Advanced AI features (Q&A, insights)

### Integration Opportunities
- **Meeting Platforms**: Zoom, Google Meet, Teams
- **Communication**: Slack, Discord, Microsoft Teams
- **File Storage**: Google Drive, Dropbox, OneDrive
- **CRM Systems**: Salesforce, HubSpot
- **Project Management**: Jira, Asana, Trello

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the AI capabilities
- FastAPI team for the excellent web framework
- Next.js team for the React framework
- All contributors and users

## 📞 Support

- 📖 Check the [SETUP.md](SETUP.md) for detailed setup instructions
- 🐛 Create an issue for bugs or feature requests
- 💬 Join discussions in the repository

---

**Built with ❤️ using FastAPI, Next.js, and OpenAI**

*Transform your team's knowledge into an intelligent, searchable resource.*
