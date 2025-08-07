"""
API Routes for Mock ERP Application
"""
import os
import requests
from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from app.models.schemas import HealthResponse, AppInfoResponse, ExternalAPIResponse
from app.application.solicitacoes import enviar_para_assistente_ia, verificar_status_assistente_ia, enviar_feedback_assistente_ia

# Create router
router = APIRouter()


# Modelo para solicitação do assistente virtual
class AssistantRequest(BaseModel):
    user: Optional[Dict[str, Any]] = None
    product: Optional[Dict[str, Any]] = None  # Para compatibilidade com versão anterior
    module: Optional[Dict[str, Any]] = None   # Nova estrutura para módulos
    userQuestion: str
    requestId: Optional[str] = None


class AssistantResponse(BaseModel):
    success: bool
    request_id: str
    local_id: Optional[str] = None
    response: Optional[str] = None
    tokens_used: Optional[int] = None
    response_time: Optional[float] = None
    error: Optional[str] = None
    fallback_response: Optional[str] = None
    categoria: Optional[str] = None
    subcategoria: Optional[str] = None


class FeedbackRequest(BaseModel):
    rating: int  # 1-5 estrelas
    feedback: Optional[str] = ""
    response_data: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None


class FeedbackResponse(BaseModel):
    success: bool
    message: str
    feedback_id: Optional[str] = None
    error: Optional[str] = None


@router.post("/api/assistant", response_model=AssistantResponse)
async def process_assistant_request(request: AssistantRequest):
    """
    Processa uma solicitação do assistente virtual
    """
    try:
        print(f"Received assistant request: {request.userQuestion}")
        print(f"User: {request.user}")
        
        # Determinar qual estrutura de dados usar (module ou product para compatibilidade)
        data_structure = request.module if request.module else request.product
        print(f"Data structure: {data_structure}")
        
        # Verificar se temos dados suficientes
        if not data_structure:
            return AssistantResponse(
                success=False,
                request_id="",
                error="Dados insuficientes: module ou product são obrigatórios",
                fallback_response="Por favor, preencha os dados do formulário antes de usar o assistente."
            )
        
        # Enviar para o assistente IA
        response = await enviar_para_assistente_ia(
            user_data=request.user,
            product_data=data_structure,  # Usar a estrutura de dados detectada
            user_question=request.userQuestion,
            request_id=request.requestId
        )
        
        # Construir resposta
        return AssistantResponse(
            success=response.get("success", False),
            request_id=response.get("request_id", ""),
            local_id=response.get("local_id"),
            response=response.get("response"),
            tokens_used=response.get("tokens_used"),
            response_time=response.get("response_time"),
            error=response.get("error"),
            fallback_response=response.get("fallback_response"),
            categoria=response.get("categoria"),
            subcategoria=response.get("subcategoria")
        )
        
    except Exception as e:
        print(f"Error processing assistant request: {e}")
        return AssistantResponse(
            success=False,
            request_id="",
            error=f"Erro interno: {str(e)}",
            fallback_response="Desculpe, ocorreu um erro ao processar sua solicitação. Tente novamente."
        )


@router.get("/api/assistant/status/{request_id}")
async def check_assistant_status(request_id: str):
    """
    Verifica o status de uma solicitação ao assistente
    """
    try:
        status = await verificar_status_assistente_ia(request_id)
        return status
    except Exception as e:
        return {"error": f"Erro ao verificar status: {str(e)}"}


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

@router.get("/api/users/")
async def get_users():
    """Get list of mock users"""
    mock_users = [
        {
            "id": 1,
            "name": "João Silva",
            "email": "joao@example.com", 
            "active": True
        },
        {
            "id": 2,
            "name": "Maria Santos",
            "email": "maria@example.com",
            "active": True
        },
        {
            "id": 3,
            "name": "Pedro Oliveira", 
            "email": "pedro@example.com",
            "active": False
        },
        {
            "id": 4,
            "name": "Ana Costa",
            "email": "ana@example.com",
            "active": True
        }
    ]
    return mock_users

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


@router.put("/api/feedback/{solicitacao_id}", response_model=FeedbackResponse)
async def submit_feedback(solicitacao_id: str, feedback_request: FeedbackRequest):
    """
    Endpoint para enviar feedback/avaliação de uma solicitação
    """
    try:
        print(f"Recebendo feedback para solicitação {solicitacao_id}: {feedback_request.rating} estrelas")
        
        resultado = await enviar_feedback_assistente_ia(
            solicitacao_id=solicitacao_id,
            avaliacao=feedback_request.rating,
            feedback_texto=feedback_request.feedback,
            dados_resposta=feedback_request.response_data
        )
        
        return FeedbackResponse(
            success=True,
            message="Feedback enviado com sucesso",
            feedback_id=resultado.get("feedback_id"),
            error=None
        )
        
    except Exception as e:
        print(f"Erro ao enviar feedback para solicitação {solicitacao_id}: {e}")
        return FeedbackResponse(
            success=False,
            message="Erro ao enviar feedback",
            error=str(e)
        )
