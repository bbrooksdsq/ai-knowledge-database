# AI Team Knowledge Base

A centralized AI-powered knowledge management system that automatically ingests, processes, and makes searchable all team interactions including call transcripts, documents, emails, and communications. Built with FastAPI, Next.js, and powered by OpenAI.

## 🚀 Live Demo

**Production URL:** [https://ai-knowledge-database-production.up.railway.app/](https://ai-knowledge-database-production.up.railway.app/)

## ✨ Features

### 🔍 **Intelligent Search**
- **Semantic Search** - Natural language queries that understand context and meaning
- **Keyword Search** - Traditional text-based search with filters
- **AI-Powered Results** - Relevant content ranked by AI understanding
- **Real-time Search** - Instant results as you type

### 📁 **Document Management**
- **Multi-Format Support** - PDFs, Word docs, text files, images
- **Drag & Drop Upload** - Simple file upload interface
- **Automatic Processing** - AI extracts content, generates summaries, and creates tags
- **Version Control** - Track document changes and updates

### 🎤 **Audio Transcription**
- **OpenAI Whisper Integration** - Automatic speech-to-text conversion
- **Speaker Identification** - AI identifies different speakers in meetings
- **Multiple Audio Formats** - MP3, WAV, M4A, FLAC support
- **Real-time Processing** - Upload and transcribe immediately

### 👥 **Microsoft Teams Integration**
- **Automatic Recording Sync** - Sync Teams meeting recordings automatically
- **Call Transcription** - All Teams calls automatically transcribed
- **Participant Tracking** - Identify who spoke when
- **Scheduled Sync** - Configure sync frequency (1-30 days)

### 🤖 **AI Processing Pipeline**
- **Content Embedding** - Vector embeddings for semantic search
- **Automatic Tagging** - AI-generated tags and categories
- **Entity Extraction** - Identify people, dates, projects, topics
- **Summary Generation** - Concise summaries of longer content
- **Smart Categorization** - Automatic content organization

### 🎨 **Modern Interface**
- **Clean, Intuitive UI** - Built with Tailwind CSS and shadcn/ui
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Real-time Updates** - Live search results and status updates
- **Tabbed Navigation** - Organized by function (Search, Upload, Transcribe, Teams, Recent)

## 🏗️ Architecture

### **Frontend**
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - Beautiful, accessible components
- **Lucide React** - Modern icon library

### **Backend**
- **FastAPI** - High-performance Python API framework
- **SQLAlchemy** - Database ORM
- **PostgreSQL** - Primary database for structured data
- **Redis** - Caching and session storage
- **Celery** - Background task processing

### **AI/ML**
- **OpenAI API** - GPT-3.5-turbo for summaries and entity extraction
- **OpenAI Whisper** - Speech-to-text transcription
- **OpenAI Embeddings** - Vector embeddings for semantic search
- **Sentence Transformers** - Local embedding fallback
- **NumPy** - Vector similarity calculations

### **Infrastructure**
- **Railway** - Cloud hosting and deployment
- **Docker** - Containerized application
- **GitHub Actions** - CI/CD pipeline
- **Environment Variables** - Secure configuration management

## 🚀 Quick Start

### **Option 1: Use the Live Demo**
Visit [https://ai-knowledge-database-production.up.railway.app/](https://ai-knowledge-database-production.up.railway.app/) and start using the system immediately.

### **Option 2: Local Development**

1. **Clone the repository**
   ```bash
   git clone https://github.com/bbrooksdsq/ai-knowledge-database.git
   cd ai-knowledge-database
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start with Docker Compose**
   ```bash
   ./start.sh
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - API Documentation: http://localhost:8000/docs

## ⚙️ Configuration

### **Required Environment Variables**

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/knowledge_base

# Redis
REDIS_URL=redis://localhost:6379

# OpenAI (Required for AI features)
OPENAI_API_KEY=sk-proj-your-openai-api-key

# Security
SECRET_KEY=your-secret-key-change-in-production
BACKEND_CORS_ORIGINS=http://localhost:3000

# Microsoft Teams Integration (Optional)
TEAMS_CLIENT_ID=your-azure-app-client-id
TEAMS_CLIENT_SECRET=your-azure-app-client-secret
TEAMS_TENANT_ID=your-azure-tenant-id
```

### **Microsoft Teams Setup**

1. **Create Azure App Registration**
   - Go to Azure Portal → App registrations → New registration
   - Name: "AI Knowledge Base Teams Integration"
   - Account types: "Accounts in this organizational directory only"

2. **Configure API Permissions**
   - Add permissions → Microsoft Graph → Application permissions
   - Add: `CallRecords.Read.All`, `Calls.Read.All`
   - Grant admin consent

3. **Create Client Secret**
   - Certificates & secrets → New client secret
   - Copy the secret value

4. **Set Environment Variables**
   - `TEAMS_CLIENT_ID`: Application (client) ID
   - `TEAMS_CLIENT_SECRET`: The secret you created
   - `TEAMS_TENANT_ID`: Directory (tenant) ID

## 📖 Usage

### **Search Your Knowledge Base**
1. Go to the **"🔍 Search"** tab
2. Choose between **Semantic Search** (AI-powered) or **Keyword Search**
3. Type your query in natural language
4. Browse results with AI-generated snippets and relevance scores

### **Upload Documents**
1. Go to the **"📤 Upload"** tab
2. Drag and drop files or click to browse
3. Documents are automatically processed with AI
4. View in the **"📅 Recent"** tab

### **Transcribe Audio**
1. Go to the **"🎤 Transcribe"** tab
2. Upload audio files (MP3, WAV, M4A, FLAC)
3. Enable speaker identification for meetings
4. Get automatic transcription with AI processing

### **Sync Teams Recordings**
1. Go to the **"👥 Teams"** tab
2. Configure Microsoft Teams integration (one-time setup)
3. Choose sync frequency (1-30 days)
4. All recordings automatically transcribed and indexed

### **View Recent Activity**
1. Go to the **"📅 Recent"** tab
2. See all recently processed documents
3. View AI-generated summaries and tags
4. Access quick actions for organization

## 🔧 API Endpoints

### **Documents**
- `GET /api/v1/documents/` - List all documents
- `POST /api/v1/documents/` - Upload new document
- `GET /api/v1/documents/{id}` - Get specific document
- `PUT /api/v1/documents/{id}` - Update document
- `DELETE /api/v1/documents/{id}` - Delete document

### **Search**
- `POST /api/v1/documents/search` - Semantic search
- `POST /api/v1/documents/search/keyword` - Keyword search
- `GET /api/v1/documents/{id}/related` - Get related documents

### **Transcription**
- `POST /api/v1/transcription/audio` - Transcribe audio file
- `POST /api/v1/transcription/test-audio` - Test Whisper API

### **Teams Integration**
- `GET /api/v1/teams/status` - Check Teams integration status
- `POST /api/v1/teams/test-connection` - Test Microsoft Graph API
- `POST /api/v1/teams/sync` - Sync Teams recordings
- `POST /api/v1/teams/sync-and-store` - Sync and store recordings

### **System**
- `GET /api/status` - System status and AI capabilities
- `GET /api/health` - Health check
- `POST /api/test/document` - Create test document

## 🛠️ Development

### **Local Development Setup**

1. **Backend Development**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

2. **Frontend Development**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Database Setup**
   ```bash
   # Start PostgreSQL and Redis
   docker-compose up -d postgres redis
   
   # Run migrations (if any)
   alembic upgrade head
   ```

### **Testing**

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### **Building for Production**

```bash
# Build Docker image
docker build -f Dockerfile.prod -t ai-knowledge-base .

# Run production container
docker run -p 8080:8080 --env-file .env ai-knowledge-base
```

## 📊 System Status

Check system capabilities at `/api/status`:

```json
{
  "api": "healthy",
  "database": "connected",
  "ai_capabilities": {
    "openai_api": true,
    "numpy": true,
    "sentence_transformers": true,
    "local_embeddings": true,
    "similarity_calculation": true
  },
  "features": {
    "document_upload": true,
    "semantic_search": true,
    "keyword_search": true,
    "ai_summaries": true,
    "ai_tags": true,
    "ai_entities": true
  }
}
```

## 🔒 Security

- **Environment Variables** - All sensitive data stored securely
- **CORS Configuration** - Proper cross-origin resource sharing
- **Input Validation** - Pydantic schemas for data validation
- **File Upload Limits** - 50MB maximum file size
- **API Authentication** - Ready for JWT token implementation

## 🚀 Deployment

### **Railway Deployment**

1. **Connect GitHub Repository**
   - Go to [Railway.app](https://railway.app)
   - Create new project from GitHub repository

2. **Configure Environment Variables**
   - Add all required environment variables
   - Set `DATABASE_URL` and `REDIS_URL` to Railway services

3. **Deploy**
   - Railway automatically builds and deploys from main branch
   - Custom domain available in Railway dashboard

### **Other Platforms**

The application can be deployed to any platform supporting Docker:
- **AWS** - ECS, EKS, or EC2
- **Google Cloud** - Cloud Run, GKE, or Compute Engine
- **Azure** - Container Instances, AKS, or App Service
- **DigitalOcean** - App Platform or Droplets
- **Heroku** - With minor configuration changes

## 📈 Roadmap

### **Completed ✅**
- [x] Core document upload and storage
- [x] AI-powered search (semantic + keyword)
- [x] OpenAI Whisper integration for audio transcription
- [x] Microsoft Teams integration for automatic recording sync
- [x] Speaker identification in audio
- [x] Automatic AI processing (summaries, tags, entities)
- [x] Modern web interface with responsive design
- [x] Production deployment on Railway

### **In Progress 🚧**
- [ ] Email integration (Gmail/Outlook)
- [ ] File storage integration (Google Drive/OneDrive)
- [ ] Webhook system for real-time ingestion
- [ ] Advanced analytics dashboard
- [ ] User management and permissions

### **Planned 📋**
- [ ] Mobile app for iOS/Android
- [ ] Advanced AI features (content generation, Q&A)
- [ ] Integration with more communication platforms
- [ ] Advanced security features
- [ ] Multi-language support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check this README and inline code comments
- **API Docs**: Visit `/docs` endpoint when running locally
- **Issues**: Create an issue on GitHub for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas

## 🙏 Acknowledgments

- **OpenAI** - For GPT, Whisper, and Embeddings APIs
- **FastAPI** - For the excellent Python web framework
- **Next.js** - For the React framework and tooling
- **Tailwind CSS** - For the utility-first CSS framework
- **Railway** - For the seamless deployment platform
- **Microsoft** - For the Graph API and Teams integration

---

**Built with ❤️ for modern teams who want to harness the power of AI for knowledge management.**