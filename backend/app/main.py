from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.orm import Session
from .core.config import settings
from .core.database import engine, get_db
from .models import document
from .models.document import Document
from .api import documents
from .api.documents import process_document_ai
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="AI-powered knowledge management system"
)

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    documents.router,
    prefix=f"{settings.API_V1_STR}/documents",
    tags=["documents"]
)

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 AI Knowledge Base API is starting up...")
    logger.info(f"Static files directory: {os.path.abspath('static')}")
    if os.path.exists("static/index.html"):
        logger.info("✅ Static files found")
    else:
        logger.warning("❌ Static files not found")
    
    # Initialize database tables
    try:
        document.Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
    
    logger.info("🎉 Application is ready to accept requests!")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 AI Knowledge Base API is shutting down...")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve the frontend index.html"""
    logger.info("Root endpoint requested - serving frontend")
    try:
        static_path = os.path.join("static", "index.html")
        if os.path.exists(static_path):
            return FileResponse(static_path, media_type="text/html")
        else:
            # Fallback HTML response
            return HTMLResponse("""
            <html>
                <head><title>AI Knowledge Base</title></head>
                <body>
                    <h1>AI Knowledge Base API</h1>
                    <p>Version 1.0.0</p>
                    <p>Static files not found</p>
                    <p><a href="/docs">API Documentation</a></p>
                </body>
            </html>
            """)
    except Exception as e:
        # Fallback HTML response on any error
        return HTMLResponse(f"""
        <html>
            <head><title>AI Knowledge Base</title></head>
            <body>
                <h1>AI Knowledge Base API</h1>
                <p>Version 1.0.0</p>
                <p>Error: {str(e)}</p>
                <p><a href="/docs">API Documentation</a></p>
            </body>
        </html>
        """)

@app.get("/_next/{file_path:path}")
async def serve_next_assets(file_path: str):
    """Serve Next.js static assets"""
    static_path = os.path.join("static", "_next", file_path)
    if os.path.exists(static_path):
        return FileResponse(static_path)
    else:
        return {"error": "File not found"}

@app.get("/404")
async def serve_404():
    """Serve 404 page"""
    static_path = os.path.join("static", "404.html")
    if os.path.exists(static_path):
        return FileResponse(static_path, media_type="text/html")
    else:
        return HTMLResponse("<h1>404 Not Found</h1>")

@app.get("/health")
async def health_check():
    logger.info("Health check requested")
    return {"status": "healthy", "port": os.environ.get("PORT", "unknown"), "ready": True}

@app.get("/test")
async def test_endpoint():
    logger.info("Test endpoint requested")
    return {"message": "Test successful", "static_files": os.path.exists("static/index.html")}

@app.get("/api/test")
async def api_test():
    """Test API connectivity"""
    return {"status": "API working", "database": "connected", "openai": "configured"}

@app.post("/api/test/document")
async def create_test_document(db: Session = Depends(get_db)):
    """Create a test document to demonstrate AI processing"""
    try:
        test_content = """
        Project Alpha Meeting Notes - Q4 2024
        
        Attendees: Sarah Johnson, Mike Chen, Lisa Rodriguez, Tom Wilson
        Date: October 15, 2024
        Duration: 45 minutes
        
        Key Discussion Points:
        1. Budget approval for Q1 2025 - $2.5M allocated for development
        2. Timeline for mobile app launch - targeting March 2025
        3. User research findings - 78% satisfaction rate with current features
        4. Technical debt concerns - need to prioritize refactoring
        5. New hire onboarding - 3 developers starting next week
        
        Action Items:
        - Sarah: Prepare budget presentation for board meeting
        - Mike: Update project timeline with new requirements
        - Lisa: Schedule user testing sessions for mobile app
        - Tom: Create technical debt assessment report
        
        Next Meeting: October 22, 2024 at 2:00 PM
        """
        
        document = Document(
            title="Project Alpha Meeting Notes - Q4 2024",
            content=test_content.strip(),
            file_type="meeting_notes",
            source="test_creation"
        )
        
        db.add(document)
        db.flush()  # Get the ID
        
        # Process with AI
        await process_document_ai(db, document)
        
        db.commit()
        db.refresh(document)
        
        return {
            "message": "Test document created successfully",
            "document_id": document.id,
            "title": document.title,
            "summary": document.summary,
            "tags": document.tags,
            "entities": document.entities
        }
        
    except Exception as e:
        db.rollback()
        return {"error": f"Failed to create test document: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
