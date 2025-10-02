from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .core.config import settings
from .api import documents
import os

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="AI-powered knowledge management system"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(
    documents.router,
    prefix=f"{settings.API_V1_STR}/documents",
    tags=["documents"]
)

@app.get("/")
async def serve_frontend():
    """Serve the frontend index.html"""
    try:
        static_path = os.path.join("static", "index.html")
        if os.path.exists(static_path):
            return FileResponse(static_path)
        else:
            # Fallback to API response if static files not found
            return {"message": "AI Knowledge Base API", "version": "1.0.0", "status": "static files not found"}
    except Exception as e:
        # Fallback to API response on any error
        return {"message": "AI Knowledge Base API", "version": "1.0.0", "error": str(e)}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
