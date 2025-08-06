"""
Exemplo de rotas para módulo de Usuários
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

# Create router with prefix and tags
router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

# Models específicos para usuários
class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    active: bool = True

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    active: bool

# Simulação de dados
fake_users_db = [
    {"id": 1, "name": "João Silva", "email": "joao@example.com", "active": True},
    {"id": 2, "name": "Maria Santos", "email": "maria@example.com", "active": True},
]

@router.get("/", response_model=List[UserResponse])
async def list_users():
    """Lista todos os usuários"""
    return fake_users_db

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Busca um usuário por ID"""
    user = next((user for user in fake_users_db if user["id"] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

@router.post("/", response_model=UserResponse)
async def create_user(user: User):
    """Cria um novo usuário"""
    new_id = max([u["id"] for u in fake_users_db]) + 1 if fake_users_db else 1
    new_user = {
        "id": new_id,
        "name": user.name,
        "email": user.email,
        "active": user.active
    }
    fake_users_db.append(new_user)
    return new_user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: User):
    """Atualiza um usuário existente"""
    user_index = next((i for i, u in enumerate(fake_users_db) if u["id"] == user_id), None)
    if user_index is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    updated_user = {
        "id": user_id,
        "name": user.name,
        "email": user.email,
        "active": user.active
    }
    fake_users_db[user_index] = updated_user
    return updated_user

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """Remove um usuário"""
    user_index = next((i for i, u in enumerate(fake_users_db) if u["id"] == user_id), None)
    if user_index is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    deleted_user = fake_users_db.pop(user_index)
    return {"message": f"Usuário {deleted_user['name']} removido com sucesso"}
