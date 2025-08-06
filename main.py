"""
Mock ERP Application
Main application entry point using FastAPI
"""
import os
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.rotas import router
from app.api.users import router as users_router

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting Mock ERP Application with FastAPI...")
    print(f"Environment: {os.getenv('FASTAPI_ENV', 'production')}")
    print(f"Debug mode: {os.getenv('FASTAPI_DEBUG', 'False')}")
    yield
    # Shutdown
    print("Shutting down Mock ERP Application...")

# Create FastAPI app
app = FastAPI(
    title="Mock ERP Application",
    description="Sistema de gestão empresarial mock usando FastAPI",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)
app.include_router(users_router)

if __name__ == "__main__":
    # Configuration
    host = "0.0.0.0"
    port = 8000
    reload = os.getenv('FASTAPI_DEBUG', 'False').lower() == 'true'
    
    print(f"Starting server at http://{host}:{port}")
    print("API Documentation available at: http://localhost:8000/docs")
    print("Alternative docs at: http://localhost:8000/redoc")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload
    )
