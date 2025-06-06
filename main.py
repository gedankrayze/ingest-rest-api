from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import logging

from app.routers import conversion

# Configure logging to match uvicorn format
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:     %(message)s'
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("MarkItDown REST API started")
    logger.info("API documentation: http://localhost:8000/docs")
    yield
    # Shutdown
    logger.info("MarkItDown REST API stopped")

app = FastAPI(
    title="MarkItDown REST API",
    description="API service for converting various file formats to Markdown using MarkItDown",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(conversion.router, prefix="/api/v1")

# Mount static files
app.mount("/static", StaticFiles(directory="public"), name="static")

@app.get("/")
async def root():
    return FileResponse("public/index.html")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_config=None)