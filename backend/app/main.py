from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from .core.config import settings
from .api import documents
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

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 AI Knowledge Base API is shutting down...")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve the frontend index.html"""
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
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
