"""
Pydantic models for Mock ERP Application
"""
from pydantic import BaseModel
from typing import Dict, Any, Optional

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    environment: str

class AppInfoResponse(BaseModel):
    """Application information response model"""
    message: str
    status: str
    version: str

class ExternalAPIResponse(BaseModel):
    """External API response model"""
    status: str
    external_data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
