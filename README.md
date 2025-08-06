# Mock ERP Teste - Master Assistant

Sistema de gestão empresarial mock desenvolvido com FastAPI e assistente virtual inteligente.

## 🚀 Funcionalidades

- **FastAPI Backend** - Framework web moderno com documentação automática de API
- **Assistente Virtual** - Sistema de diálogo inteligente que coleta dados de produtos e fornece assistência com IA
- **Gestão de Produtos** - Sistema completo de cadastro de produtos com 6 categorias (Eletrônicos, Roupas, Casa & Jardim, Esportes, Livros, Saúde & Beleza)
- **Frontend Moderno** - Interface HTML/CSS/JavaScript responsiva com design profissional
- **Integração de APIs** - Pronto para consumo de APIs externas e integração com serviços de IA
- **Configuração de Ambiente** - Gerenciamento flexível de configurações
- **Suporte CORS** - Compartilhamento de recursos entre origens habilitado
- **Monitoramento** - Endpoints de health check integrados

## 🛠️ Tecnologias Utilizadas

- **Backend**: FastAPI 0.116.1, Uvicorn, Pydantic
- **Frontend**: HTML5, CSS3 (Grid/Flexbox), JavaScript Vanilla
- **Python**: 3.13.4 com ambiente virtual
- **Cliente API**: Requests, HTTPX
- **Processamento de Dados**: Pandas, NumPy
- **Configuração**: python-dotenv

## 📁 Estrutura do Projeto

```
Mock_Erp/
├── app/
│   ├── application/     # Lógica de aplicação
│   ├── api/            # Endpoints da API
│   │   ├── __init__.py
│   │   ├── rotas.py    # Rotas principais
│   │   └── users.py    # Rotas de usuários (exemplo)
│   ├── models/         # Modelos de dados
│   │   ├── __init__.py
│   │   └── schemas.py  # Schemas Pydantic
│   └── templates/      # Templates HTML
├── venv/               # Ambiente virtual
├── main.py             # Aplicação FastAPI principal
├── requirements.txt    # Dependências
├── .env               # Variáveis de ambiente
└── start.bat          # Script de inicialização
```

## 🛠️ Instalação e Configuração

### 1. Ativar o ambiente virtual
```bash
.\venv\Scripts\Activate.ps1
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente
Copie `.env.example` para `.env` e ajuste as configurações conforme necessário.

## 🚀 Executando a Aplicação

### Método 1: Script automático
```bash
.\start.bat
```

### Método 2: Comando manual
```bash
.\venv\Scripts\Activate.ps1
python main.py
```

### Método 3: Uvicorn direto
```bash
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📡 Endpoints Disponíveis

### Rotas Principais
- **GET /** - Informações básicas da aplicação
- **GET /api/health** - Health check
- **GET /api/test-external** - Teste de consumo de API externa
- **GET /dashboard** - Dashboard HTML

### Rotas de Usuários (Exemplo)
- **GET /api/users/** - Lista todos os usuários
- **GET /api/users/{user_id}** - Busca usuário por ID
- **POST /api/users/** - Cria novo usuário
- **PUT /api/users/{user_id}** - Atualiza usuário
- **DELETE /api/users/{user_id}** - Remove usuário

### Documentação
- **GET /docs** - Documentação automática da API (Swagger)
- **GET /redoc** - Documentação alternativa (ReDoc)

## 🌐 Acessos

Após iniciar a aplicação:

- **Aplicação Principal:** http://localhost:8000
- **Dashboard:** http://localhost:8000/dashboard
- **Documentação da API:** http://localhost:8000/docs
- **Documentação Alternativa:** http://localhost:8000/redoc

## 🧪 Testando a API

### Via curl:
```bash
# Health check
curl http://localhost:8000/api/health

# Teste de API externa
curl http://localhost:8000/api/test-external
```

### Via navegador:
Acesse http://localhost:8000/docs para interface interativa da API.

## 🔧 Desenvolvimento

### Estrutura recomendada para desenvolvimento:

1. **Modelos** - Definir em `app/models/`
2. **Routers** - Criar em `app/api/`
3. **Business Logic** - Implementar em `app/application/`
4. **Templates** - Adicionar em `app/templates/`

### Exemplo de adição de novo endpoint:

```python
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ItemModel(BaseModel):
    name: str
    description: str

@router.post("/items/")
async def create_item(item: ItemModel):
    return {"message": "Item created", "item": item}
```

## 📝 Vantagens do FastAPI

- ✅ **Performance** - Um dos frameworks mais rápidos disponíveis
- ✅ **Documentação Automática** - Swagger UI e ReDoc integrados
- ✅ **Type Hints** - Validação automática de tipos com Pydantic
- ✅ **Async Support** - Suporte nativo para operações assíncronas
- ✅ **Modern Python** - Baseado em Python 3.7+ e type hints
- ✅ **Standards-based** - OpenAPI, JSON Schema
