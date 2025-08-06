"""
API Routes for Mock ERP Application
"""
import os
import requests
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from app.models.schemas import HealthResponse, AppInfoResponse, ExternalAPIResponse

# Create router
router = APIRouter()

@router.get("/", response_model=AppInfoResponse)
async def home():
    """Home page route"""
    return AppInfoResponse(
        message="Mock ERP Application",
        status="running",
        version="1.0.0"
    )

@router.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        environment=os.getenv('FASTAPI_ENV', 'production')
    )

@router.get("/api/test-external", response_model=ExternalAPIResponse)
async def test_external_api():
    """Test endpoint for consuming external APIs"""
    try:
        # Example: consuming a test API
        response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
        response.raise_for_status()
        data = response.json()
        
        return ExternalAPIResponse(
            status="success",
            external_data=data
        )
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"External API error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal error: {str(e)}"
        )

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Serve the dashboard HTML page"""
    try:
        with open("app/templates/index.html", "r", encoding="utf-8") as file:
            return HTMLResponse(content=file.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Dashboard template not found")
