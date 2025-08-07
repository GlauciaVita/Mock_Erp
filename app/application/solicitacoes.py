"""
Módulo de Solicitações - Mock ERP Application
Gerencia as solicitações e interações do sistema
"""
from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
import uuid
import httpx
import asyncio
import time


class SolicitacaoCreate(BaseModel):
    """Modelo para criação de solicitações seguindo o padrão do assistente de IA"""
    nome_assistente: Optional[str] = None  # Será definido automaticamente
    solicitacao_usuario: str
    resposta_assistente: str
    erro: Optional[str] = None
    usuario_id: Optional[str] = None
    contexto_conversa: Optional[str] = None
    historico_mensagens: Optional[List[str]] = []
    intent_detectado: Optional[str] = None
    entidades_extraidas: Optional[List[str]] = []
    confianca_resposta: Optional[float] = None
    tokens_utilizados: Optional[int] = None
    modelo_utilizado: Optional[str] = "gpt-3.5-turbo"
    temperatura: Optional[float] = 0.7
    prompt_utilizado: Optional[str] = None
    categoria_solicitacao: Optional[str] = None
    subcategoria: Optional[str] = None
    complexidade: Optional[str] = None
    sentimento: Optional[str] = None
    avaliacao_usuario: Optional[int] = None
    feedback_texto: Optional[str] = None
    usuario_satisfeito: Optional[bool] = None
    precisou_escalacao: Optional[bool] = False
    resolveu_problema: Optional[bool] = None
    tipo_problema: Optional[str] = None
    solucao_aplicada: Optional[str] = None
    palavras_chave: Optional[List[str]] = []
    topicos_abordados: Optional[List[str]] = []
    competencias_utilizadas: Optional[List[str]] = []
    endpoint_utilizado: Optional[str] = None
    versao_assistente: Optional[str] = None
    tags: Optional[List[str]] = []


class SolicitacaoBase(BaseModel):
    """Modelo base para solicitações"""
    id: Optional[str] = None
    user_id: Optional[int] = None
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    tipo: str  # 'assistente_virtual', 'produto', 'suporte', etc.
    status: str = 'pendente'  # 'pendente', 'processando', 'concluida', 'erro'
    prioridade: str = 'normal'  # 'baixa', 'normal', 'alta', 'urgente'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class SolicitacaoAssistenteVirtual(SolicitacaoBase):
    """Solicitação específica para o assistente virtual"""
    pergunta: str
    contexto_produto: Optional[Dict[str, Any]] = None
    resposta: Optional[str] = None
    tokens_utilizados: Optional[int] = None
    tempo_resposta: Optional[float] = None


class SolicitacaoProduto(SolicitacaoBase):
    """Solicitação relacionada a produtos"""
    produto_id: Optional[str] = None
    produto_nome: Optional[str] = None
    acao: str  # 'criar', 'atualizar', 'excluir', 'consultar'
    dados_produto: Optional[Dict[str, Any]] = None
    observacoes: Optional[str] = None


class SolicitacaoSuporte(SolicitacaoBase):
    """Solicitação de suporte técnico"""
    categoria: str  # 'bug', 'feature', 'duvida', 'melhoria'
    descricao: str
    arquivos_anexos: Optional[List[str]] = None
    nivel_urgencia: str = 'normal'


# Simulação de banco de dados em memória
solicitacoes_db: List[Dict[str, Any]] = []


class GerenciadorSolicitacoes:
    """Classe para gerenciar solicitações do sistema"""
    
    @staticmethod
    def gerar_id() -> str:
        """Gera um ID único para a solicitação"""
        return f"SOL_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
    
    @staticmethod
    def criar_solicitacao_assistente(
        user_id: Optional[int],
        user_name: Optional[str],
        user_email: Optional[str],
        pergunta: str,
        contexto_produto: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Cria uma nova solicitação para o assistente virtual"""
        
        solicitacao = {
            "id": GerenciadorSolicitacoes.gerar_id(),
            "user_id": user_id,
            "user_name": user_name,
            "user_email": user_email,
            "tipo": "assistente_virtual",
            "status": "pendente",
            "prioridade": "normal",
            "pergunta": pergunta,
            "contexto_produto": contexto_produto,
            "resposta": None,
            "tokens_utilizados": None,
            "tempo_resposta": None,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        solicitacoes_db.append(solicitacao)
        return solicitacao
    
    @staticmethod
    def criar_solicitacao_produto(
        user_id: Optional[int],
        user_name: Optional[str],
        user_email: Optional[str],
        acao: str,
        produto_id: Optional[str] = None,
        produto_nome: Optional[str] = None,
        dados_produto: Optional[Dict[str, Any]] = None,
        observacoes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Cria uma nova solicitação relacionada a produtos"""
        
        solicitacao = {
            "id": GerenciadorSolicitacoes.gerar_id(),
            "user_id": user_id,
            "user_name": user_name,
            "user_email": user_email,
            "tipo": "produto",
            "status": "pendente",
            "prioridade": "normal",
            "acao": acao,
            "produto_id": produto_id,
            "produto_nome": produto_nome,
            "dados_produto": dados_produto,
            "observacoes": observacoes,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        solicitacoes_db.append(solicitacao)
        return solicitacao
    
    @staticmethod
    def criar_solicitacao_suporte(
        user_id: Optional[int],
        user_name: Optional[str],
        user_email: Optional[str],
        categoria: str,
        descricao: str,
        nivel_urgencia: str = "normal",
        arquivos_anexos: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Cria uma nova solicitação de suporte"""
        
        solicitacao = {
            "id": GerenciadorSolicitacoes.gerar_id(),
            "user_id": user_id,
            "user_name": user_name,
            "user_email": user_email,
            "tipo": "suporte",
            "status": "pendente",
            "prioridade": nivel_urgencia,
            "categoria": categoria,
            "descricao": descricao,
            "arquivos_anexos": arquivos_anexos or [],
            "nivel_urgencia": nivel_urgencia,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        solicitacoes_db.append(solicitacao)
        return solicitacao
    
    @staticmethod
    def buscar_solicitacao(solicitacao_id: str) -> Optional[Dict[str, Any]]:
        """Busca uma solicitação pelo ID"""
        return next((sol for sol in solicitacoes_db if sol["id"] == solicitacao_id), None)
    
    @staticmethod
    def listar_solicitacoes(
        user_id: Optional[int] = None,
        tipo: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Lista solicitações com filtros opcionais"""
        
        solicitacoes = solicitacoes_db.copy()
        
        if user_id:
            solicitacoes = [sol for sol in solicitacoes if sol.get("user_id") == user_id]
        
        if tipo:
            solicitacoes = [sol for sol in solicitacoes if sol.get("tipo") == tipo]
        
        if status:
            solicitacoes = [sol for sol in solicitacoes if sol.get("status") == status]
        
        # Ordenar por data de criação (mais recentes primeiro)
        solicitacoes.sort(key=lambda x: x.get("created_at", datetime.min), reverse=True)
        
        return solicitacoes[:limit]
    
    @staticmethod
    def atualizar_status(solicitacao_id: str, novo_status: str) -> bool:
        """Atualiza o status de uma solicitação"""
        solicitacao = GerenciadorSolicitacoes.buscar_solicitacao(solicitacao_id)
        if solicitacao:
            solicitacao["status"] = novo_status
            solicitacao["updated_at"] = datetime.now()
            return True
        return False
    
    @staticmethod
    def atualizar_resposta_assistente(
        solicitacao_id: str,
        resposta: str,
        tokens_utilizados: Optional[int] = None,
        tempo_resposta: Optional[float] = None
    ) -> bool:
        """Atualiza a resposta de uma solicitação do assistente virtual"""
        solicitacao = GerenciadorSolicitacoes.buscar_solicitacao(solicitacao_id)
        if solicitacao and solicitacao.get("tipo") == "assistente_virtual":
            solicitacao["resposta"] = resposta
            solicitacao["tokens_utilizados"] = tokens_utilizados
            solicitacao["tempo_resposta"] = tempo_resposta
            solicitacao["status"] = "concluida"
            solicitacao["updated_at"] = datetime.now()
            return True
        return False
    
    @staticmethod
    def obter_estatisticas() -> Dict[str, Any]:
        """Retorna estatísticas das solicitações"""
        total = len(solicitacoes_db)
        
        if total == 0:
            return {
                "total": 0,
                "por_status": {},
                "por_tipo": {},
                "por_prioridade": {}
            }
        
        # Contar por status
        status_count = {}
        for sol in solicitacoes_db:
            status = sol.get("status", "pendente")
            status_count[status] = status_count.get(status, 0) + 1
        
        # Contar por tipo
        tipo_count = {}
        for sol in solicitacoes_db:
            tipo = sol.get("tipo", "indefinido")
            tipo_count[tipo] = tipo_count.get(tipo, 0) + 1
        
        # Contar por prioridade
        prioridade_count = {}
        for sol in solicitacoes_db:
            prioridade = sol.get("prioridade", "normal")
            prioridade_count[prioridade] = prioridade_count.get(prioridade, 0) + 1
        
        return {
            "total": total,
            "por_status": status_count,
            "por_tipo": tipo_count,
            "por_prioridade": prioridade_count,
            "ultima_atualizacao": datetime.now()
        }


# Funções auxiliares para uso direto
def criar_solicitacao_assistente_virtual(
    user_data: Optional[Dict[str, Any]],
    pergunta: str,
    contexto_produto: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Função helper para criar solicitação do assistente virtual"""
    user_id = user_data.get("id") if user_data else None
    user_name = user_data.get("name") if user_data else None
    user_email = user_data.get("email") if user_data else None
    
    return GerenciadorSolicitacoes.criar_solicitacao_assistente(
        user_id=user_id,
        user_name=user_name,
        user_email=user_email,
        pergunta=pergunta,
        contexto_produto=contexto_produto
    )


def processar_solicitacao_assistente(solicitacao_id: str) -> Dict[str, Any]:
    """Processa uma solicitação do assistente virtual (simulação)"""
    solicitacao = GerenciadorSolicitacoes.buscar_solicitacao(solicitacao_id)
    
    if not solicitacao:
        return {"erro": "Solicitação não encontrada"}
    
    if solicitacao.get("tipo") != "assistente_virtual":
        return {"erro": "Tipo de solicitação inválido"}
    
    # Atualizar status para processando
    GerenciadorSolicitacoes.atualizar_status(solicitacao_id, "processando")
    
    # Simular processamento (aqui seria a integração com IA)
    pergunta = solicitacao.get("pergunta", "")
    contexto = solicitacao.get("contexto_produto", {})
    
    # Resposta simulada baseada no contexto
    resposta_simulada = gerar_resposta_simulada(pergunta, contexto)
    
    # Atualizar com a resposta
    GerenciadorSolicitacoes.atualizar_resposta_assistente(
        solicitacao_id=solicitacao_id,
        resposta=resposta_simulada,
        tokens_utilizados=len(resposta_simulada.split()) * 2,  # Simulação
        tempo_resposta=1.5  # Simulação
    )
    
    return GerenciadorSolicitacoes.buscar_solicitacao(solicitacao_id)


def gerar_resposta_simulada(pergunta: str, contexto: Dict[str, Any]) -> str:
    """Gera uma resposta simulada para o assistente virtual"""
    
    produto = contexto.get("product", {}) if contexto else {}
    produto_nome = produto.get("name", "produto")
    produto_categoria = produto.get("category", "categoria não especificada")
    
    pergunta_lower = pergunta.lower()
    
    if "preço" in pergunta_lower or "custo" in pergunta_lower:
        return f"Para definir o preço do {produto_nome}, considere: custo de produção + margem de lucro desejada + impostos. Para produtos da categoria {produto_categoria}, sugiro pesquisar preços de concorrentes e aplicar uma margem entre 30-50%."
    
    elif "estoque" in pergunta_lower or "quantidade" in pergunta_lower:
        return f"Para gestão de estoque do {produto_nome}, recomendo: monitorar o giro de estoque, definir ponto de reposição e manter estoque de segurança. Produtos da categoria {produto_categoria} geralmente têm boa rotatividade."
    
    elif "venda" in pergunta_lower or "marketing" in pergunta_lower:
        return f"Para melhorar as vendas do {produto_nome}, sugiro: destacar os benefícios únicos, criar campanhas segmentadas para {produto_categoria}, e considerar promoções sazonais."
    
    elif "fornecedor" in pergunta_lower:
        return f"Para encontrar fornecedores do {produto_nome}, recomendo: pesquisar no Alibaba, contatar distribuidores locais, e verificar feiras do setor de {produto_categoria}."
    
    elif "cadastro" in pergunta_lower or "registro" in pergunta_lower:
        return f"Para cadastrar o {produto_nome} corretamente: preencha todos os campos obrigatórios, inclua descrição detalhada, defina a categoria como {produto_categoria}, e adicione fotos de qualidade."
    
    else:
        return f"Entendi sua dúvida sobre o {produto_nome}. Para produtos da categoria {produto_categoria}, recomendo verificar as melhores práticas do setor e consultar nossa base de conhecimento. Posso ajudar com informações mais específicas se você detalhar sua necessidade."


# Funções auxiliares para análise de solicitações
def detectar_categoria_solicitacao(pergunta: str) -> str:
    """Detecta a categoria da solicitação baseada na pergunta"""
    pergunta_lower = pergunta.lower()
    
    if any(palavra in pergunta_lower for palavra in ["preço", "custo", "valor", "dinheiro"]):
        return "pricing"
    elif any(palavra in pergunta_lower for palavra in ["estoque", "quantidade", "inventário"]):
        return "inventory"
    elif any(palavra in pergunta_lower for palavra in ["venda", "marketing", "cliente"]):
        return "sales_marketing"
    elif any(palavra in pergunta_lower for palavra in ["fornecedor", "compra", "aquisição"]):
        return "procurement"
    elif any(palavra in pergunta_lower for palavra in ["cadastro", "registro", "dados"]):
        return "data_management"
    elif any(palavra in pergunta_lower for palavra in ["relatório", "análise", "dashboard"]):
        return "reporting"
    else:
        return "general_inquiry"


def detectar_subcategoria_solicitacao(pergunta: str, product_data: Dict[str, Any]) -> str:
    """Detecta a subcategoria baseada na pergunta e dados do produto"""
    categoria = detectar_categoria_solicitacao(pergunta)
    product_category = product_data.get("category", "")
    
    if categoria == "pricing":
        return f"pricing_{product_category}" if product_category else "pricing_general"
    elif categoria == "inventory":
        return f"inventory_{product_category}" if product_category else "inventory_general"
    elif categoria == "sales_marketing":
        return f"sales_{product_category}" if product_category else "sales_general"
    else:
        return f"{categoria}_general"


def extrair_palavras_chave(pergunta: str) -> List[str]:
    """Extrai palavras-chave relevantes da pergunta"""
    import re
    
    # Remover pontuação e converter para minúsculas
    pergunta_limpa = re.sub(r'[^\w\s]', '', pergunta.lower())
    palavras = pergunta_limpa.split()
    
    # Palavras irrelevantes (stop words)
    stop_words = {
        "o", "a", "os", "as", "um", "uma", "de", "da", "do", "das", "dos", 
        "em", "na", "no", "nas", "nos", "para", "por", "com", "como", 
        "que", "qual", "quando", "onde", "porque", "este", "esta", "isso",
        "é", "são", "foi", "será", "tem", "ter", "posso", "pode", "deve"
    }
    
    # Filtrar palavras relevantes
    palavras_relevantes = [palavra for palavra in palavras 
                          if len(palavra) > 2 and palavra not in stop_words]
    
    return list(set(palavras_relevantes))[:10]  # Máximo 10 palavras-chave únicas


def extrair_topicos_abordados(pergunta: str, product_data: Dict[str, Any]) -> List[str]:
    """Extrai tópicos abordados na pergunta"""
    topicos = []
    pergunta_lower = pergunta.lower()
    
    # Tópicos baseados na pergunta
    topicos_map = {
        "preço": ["pricing", "cost_analysis"],
        "custo": ["pricing", "cost_analysis"],
        "estoque": ["inventory_management", "stock_control"],
        "venda": ["sales_strategy", "customer_engagement"],
        "marketing": ["marketing_strategy", "promotion"],
        "fornecedor": ["supplier_management", "procurement"],
        "cadastro": ["data_entry", "product_registration"],
        "categoria": ["categorization", "product_classification"]
    }
    
    for palavra, topics in topicos_map.items():
        if palavra in pergunta_lower:
            topicos.extend(topics)
    
    # Adicionar tópico da categoria do produto
    if product_data.get("category"):
        topicos.append(f"product_{product_data['category']}")
    
    return list(set(topicos))


def extrair_entidades(pergunta: str, product_data: Dict[str, Any]) -> List[str]:
    """Extrai entidades mencionadas na pergunta"""
    entidades = []
    
    # Adicionar dados do produto como entidades
    if product_data.get("name"):
        entidades.append(f"PRODUCT:{product_data['name']}")
    
    if product_data.get("category"):
        entidades.append(f"CATEGORY:{product_data['category']}")
    
    if product_data.get("code"):
        entidades.append(f"CODE:{product_data['code']}")
    
    # Detectar valores monetários
    import re
    valores = re.findall(r'R\$\s*\d+(?:,\d{2})?|\d+\s*reais?', pergunta, re.IGNORECASE)
    for valor in valores:
        entidades.append(f"MONEY:{valor}")
    
    # Detectar números/quantidades
    numeros = re.findall(r'\d+', pergunta)
    for numero in numeros[:3]:  # Máximo 3 números
        entidades.append(f"NUMBER:{numero}")
    
    return entidades


def detectar_complexidade(pergunta: str) -> str:
    """Detecta a complexidade da pergunta"""
    pergunta_lower = pergunta.lower()
    
    # Indicadores de alta complexidade
    alta_complexidade = [
        "como integrar", "análise detalhada", "estratégia", "implementar",
        "otimizar", "automatizar", "processo completo", "workflow"
    ]
    
    # Indicadores de baixa complexidade
    baixa_complexidade = [
        "o que é", "como faço", "onde encontro", "qual valor", "quanto custa"
    ]
    
    if any(indicador in pergunta_lower for indicador in alta_complexidade):
        return "alta"
    elif any(indicador in pergunta_lower for indicador in baixa_complexidade):
        return "baixa"
    elif len(pergunta.split()) > 15:
        return "media"
    else:
        return "baixa"


def detectar_sentimento(pergunta: str) -> str:
    """Detecta o sentimento da pergunta"""
    pergunta_lower = pergunta.lower()
    
    # Palavras positivas
    positivas = ["ótimo", "excelente", "bom", "gosto", "adorei", "perfeito"]
    
    # Palavras negativas
    negativas = ["problema", "erro", "ruim", "não funciona", "difícil", "complicado"]
    
    # Palavras neutras/questionamento
    neutras = ["como", "onde", "quando", "qual", "preciso", "quero", "gostaria"]
    
    if any(palavra in pergunta_lower for palavra in positivas):
        return "positivo"
    elif any(palavra in pergunta_lower for palavra in negativas):
        return "negativo"
    elif any(palavra in pergunta_lower for palavra in neutras):
        return "neutro"
    else:
        return "neutro"


def gerar_tags(pergunta: str, product_data: Dict[str, Any]) -> List[str]:
    """Gera tags relevantes para a solicitação"""
    tags = []
    
    # Tags baseadas na categoria do produto
    if product_data.get("category"):
        tags.append(product_data["category"])
    
    # Tags baseadas na pergunta
    pergunta_lower = pergunta.lower()
    
    tags_map = {
        "preço": ["pricing", "cost"],
        "estoque": ["inventory", "stock"],
        "venda": ["sales", "revenue"],
        "marketing": ["marketing", "promotion"],
        "fornecedor": ["supplier", "vendor"],
        "cadastro": ["registration", "data"],
        "urgente": ["urgent", "priority"],
        "importante": ["important", "critical"]
    }
    
    for palavra, tag_list in tags_map.items():
        if palavra in pergunta_lower:
            tags.extend(tag_list)
    
    # Tags do tipo de produto
    product_type = product_data.get("selectedType", "")
    if "eletrônico" in product_type.lower():
        tags.extend(["electronics", "technology"])
    elif "roupa" in product_type.lower():
        tags.extend(["clothing", "fashion"])
    elif "livro" in product_type.lower():
        tags.extend(["books", "education"])
    
    # Adicionar tag do sistema
    tags.append("mock_erp")
    
    return list(set(tags))[:10]  # Máximo 10 tags únicas


def determinar_tela_atual(product_data: Dict[str, Any]) -> str:
    """
    Determina a tela/módulo atual baseado nos dados do produto/módulo
    
    Args:
        product_data: Dados do produto ou módulo atual
        
    Returns:
        String identificando a tela atual
    """
    # Verificar se é um módulo específico
    if isinstance(product_data, dict):
        module_type = product_data.get("type", "")
        
        if module_type == "Clientes":
            return "clientes"
        elif module_type == "Vendas":
            return "vendas"
        elif module_type == "Transportadoras":
            return "transportadoras"
        elif module_type == "Notas Fiscais":
            return "notas_fiscais"
        elif module_type == "Usuários":
            return "usuarios"
        elif module_type == "Empresa":
            return "empresa"
        elif module_type == "Produtos":
            return "produtos"
        
        # Se tem categoria de produto, é tela de produtos
        if product_data.get("category"):
            return "produtos"
            
        # Se tem dados de cliente
        if any(key in product_data for key in ["clienteNome", "clienteTipo", "clienteDocumento"]):
            return "clientes"
            
        # Se tem dados de venda
        if any(key in product_data for key in ["vendaNumero", "vendaCliente", "vendaTotal"]):
            return "vendas"
            
        # Se tem dados de transportadora
        if any(key in product_data for key in ["transpNome", "transpCnpj", "transpRegiao"]):
            return "transportadoras"
            
        # Se tem dados de nota fiscal
        if any(key in product_data for key in ["nfNumero", "nfSerie", "nfTipo"]):
            return "notas_fiscais"
            
        # Se tem dados de usuário
        if any(key in product_data for key in ["usuarioNome", "usuarioLogin", "usuarioPerfil"]):
            return "usuarios"
            
        # Se tem dados de empresa
        if any(key in product_data for key in ["empresaNome", "empresaCnpj", "empresaFantasia"]):
            return "empresa"
    
    # Default para produtos se não conseguir determinar
    return "produtos"


async def enviar_para_assistente_ia(
    user_data: Optional[Dict[str, Any]],
    product_data: Dict[str, Any],
    user_question: str,
    request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Envia os dados para o endpoint /solicitacoes do assistente de IA na porta 8001
    
    Args:
        user_data: Dados do usuário (id, name, email, active)
        product_data: Dados do produto (code, name, category, description, etc.)
        user_question: Pergunta/dúvida do usuário
        request_id: ID único da solicitação (gerado automaticamente se não fornecido)
    
    Returns:
        Dict com a resposta do assistente ou erro
    """
    
    # URL do endpoint do assistente de IA
    ASSISTENTE_IA_URL = "http://localhost:8001/solicitacoes/executar"
    
    # Gerar ID se não fornecido
    if not request_id:
        request_id = GerenciadorSolicitacoes.gerar_id()
    
    # Extrair informações do usuário
    usuario_id = str(user_data.get("id")) if user_data and user_data.get("id") else None
    usuario_nome = user_data.get("name") if user_data else "Usuário Anônimo"
    
    # Criar contexto da conversa com informações do produto
    contexto_conversa = {
        "usuario": user_data,
        "produto": product_data,
        "sessao_id": f"erp_session_{int(time.time())}",
        "origem": "mock_erp_dashboard",
        "timestamp": datetime.now().isoformat()
    }
    
    # Detectar categoria e subcategoria baseada na pergunta
    categoria_solicitacao = detectar_categoria_solicitacao(user_question)
    subcategoria = detectar_subcategoria_solicitacao(user_question, product_data)
    
    # Extrair palavras-chave e tópicos
    palavras_chave = extrair_palavras_chave(user_question)
    topicos_abordados = extrair_topicos_abordados(user_question, product_data)
    
    # Determinar a tela/módulo atual baseado no tipo de produto
    tela_atual = determinar_tela_atual(product_data)
    
    # Preparar payload completo seguindo o formato esperado pela API
    payload = {
        "solicitacao_usuario": user_question,
        "usuario_id": usuario_id,
        "contexto_conversa": f"Usuário {usuario_nome} consultando sobre produto {product_data.get('name', 'N/A')} da categoria {product_data.get('category', 'N/A')}",
        "historico_mensagens": [user_question],
        "categoria_solicitacao": categoria_solicitacao,
        "tags": gerar_tags(user_question, product_data),
        "produto_nome": product_data.get("name", ""),
        "produto_categoria": product_data.get("category", ""),
        "complexidade": detectar_complexidade(user_question),
        "sentimento": detectar_sentimento(user_question),
        "palavras_chave": palavras_chave,
        "topicos_abordados": topicos_abordados,
        # Campos obrigatórios adicionais
        "tela": tela_atual,
        "resposta_assistente": ""  # Campo obrigatório, será preenchido pela IA
    }
    
    try:
        # Criar solicitação local antes de enviar
        solicitacao_local = criar_solicitacao_assistente_virtual(
            user_data=user_data,
            pergunta=user_question,
            contexto_produto={"product": product_data}
        )
        
        # Atualizar status para processando
        GerenciadorSolicitacoes.atualizar_status(solicitacao_local["id"], "processando")
        
        # Log do payload que será enviado
        print(f"📤 Enviando payload para IA: {payload}")
        
        # Fazer a requisição para o assistente de IA
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                ASSISTENTE_IA_URL,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "MockERP/1.0",
                    "X-Request-Source": "mock_erp",
                    "X-Request-ID": request_id
                }
            )
            
            if response.status_code == 200:
                resposta_ia = response.json()
                print(f"📥 Resposta recebida da IA: {resposta_ia}")
                
                # Extrair dados do formato específico da resposta
                execucao = resposta_ia.get("execucao", {})
                processamento = resposta_ia.get("processamento", {})
                solicitacao_salva = resposta_ia.get("solicitacao_salva", {})
                
                print(f"🎯 Execução: {execucao}")
                print(f"⚙️ Processamento: {processamento}")
                print(f"💾 Solicitação Salva: {solicitacao_salva}")
                
                # Atualizar solicitação local com a resposta
                # A resposta está em execucao.resposta
                resposta_texto = execucao.get("resposta", "")
                if not resposta_texto:
                    resposta_texto = execucao.get("resposta_assistente", "")
                if not resposta_texto:
                    resposta_texto = "Resposta não disponível"
                    
                tokens_utilizados = execucao.get("tokens_utilizados", 0)
                tempo_resposta = processamento.get("tempo_processamento", 0.0)
                
                # Usar o ID da solicitacao_salva como identificador para feedback
                solicitacao_id_ia = solicitacao_salva.get("id", "")
                
                GerenciadorSolicitacoes.atualizar_resposta_assistente(
                    solicitacao_id=solicitacao_local["id"],
                    resposta=resposta_texto,
                    tokens_utilizados=tokens_utilizados,
                    tempo_resposta=tempo_resposta
                )
                
                return {
                    "success": True,
                    "request_id": request_id,
                    "local_id": solicitacao_id_ia,  # Usar ID da IA para feedback
                    "response": resposta_texto,
                    "tokens_used": tokens_utilizados,
                    "response_time": tempo_resposta,
                    "ia_response": resposta_ia,
                    "categoria": processamento.get("categoria_detectada", categoria_solicitacao),
                    "subcategoria": subcategoria,
                    "execucao": execucao,
                    "processamento": processamento,
                    "solicitacao_salva": solicitacao_salva
                }
            
            else:
                # Erro na resposta da IA
                print(f"❌ Erro na API de IA: Status {response.status_code}")
                print(f"📄 Resposta: {response.text}")
                error_msg = f"Erro na API de IA: {response.status_code} - {response.text}"
                GerenciadorSolicitacoes.atualizar_status(solicitacao_local["id"], "erro")
                
                return {
                    "success": False,
                    "error": error_msg,
                    "request_id": request_id,
                    "local_id": solicitacao_local["id"],
                    "fallback_response": gerar_resposta_simulada(user_question, {"product": product_data})
                }
    
    except httpx.TimeoutException:
        # Timeout na requisição
        print(f"⏰ Timeout na conexão com o assistente de IA")
        error_msg = "A solicitação demorou mais que o esperado. Por favor, tente novamente."
        if 'solicitacao_local' in locals():
            GerenciadorSolicitacoes.atualizar_status(solicitacao_local["id"], "erro")
        
        return {
            "success": False,
            "error": error_msg,
            "request_id": request_id,
            "local_id": solicitacao_local["id"] if 'solicitacao_local' in locals() else None,
            "timeout": True  # Indicador específico de timeout
        }
    
    except httpx.ConnectError:
        # Erro de conexão (serviço indisponível)
        print(f"🔌 Erro de conexão: Assistente de IA indisponível na URL {ASSISTENTE_IA_URL}")
        error_msg = "Não foi possível conectar ao assistente de IA. Verifique se o serviço está rodando e tente novamente."
        if 'solicitacao_local' in locals():
            GerenciadorSolicitacoes.atualizar_status(solicitacao_local["id"], "erro")
        
        return {
            "success": False,
            "error": error_msg,
            "request_id": request_id,
            "local_id": solicitacao_local["id"] if 'solicitacao_local' in locals() else None,
            "connection_error": True  # Indicador específico de erro de conexão
        }
    
    except Exception as e:
        # Erro geral
        error_msg = f"Erro inesperado ao processar solicitação: {str(e)}. Tente novamente."
        if 'solicitacao_local' in locals():
            GerenciadorSolicitacoes.atualizar_status(solicitacao_local["id"], "erro")
        
        return {
            "success": False,
            "error": error_msg,
            "request_id": request_id,
            "local_id": solicitacao_local["id"] if 'solicitacao_local' in locals() else None,
            "unexpected_error": True  # Indicador específico de erro inesperado
        }


def enviar_para_assistente_ia_sync(
    user_data: Optional[Dict[str, Any]],
    product_data: Dict[str, Any],
    user_question: str,
    request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Versão síncrona da função para enviar dados ao assistente de IA
    Útil para uso em contextos que não suportam async/await
    """
    try:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(
            enviar_para_assistente_ia(user_data, product_data, user_question, request_id)
        )
    except RuntimeError:
        # Se não há loop em execução, criar um novo
        return asyncio.run(
            enviar_para_assistente_ia(user_data, product_data, user_question, request_id)
        )


def verificar_status_assistente_ia() -> Dict[str, Any]:
    """
    Verifica se o serviço de assistente de IA está disponível
    """
    try:
        import requests
        response = requests.get("http://localhost:8001/health", timeout=5)
        if response.status_code == 200:
            return {
                "available": True,
                "status": "online",
                "response_time": response.elapsed.total_seconds(),
                "service_info": response.json() if response.headers.get("content-type", "").startswith("application/json") else None
            }
        else:
            return {
                "available": False,
                "status": "error",
                "error": f"HTTP {response.status_code}"
            }
    except Exception as e:
        return {
            "available": False,
            "status": "offline",
            "error": str(e)
        }


async def enviar_feedback_assistente_ia(
    solicitacao_id: str,
    avaliacao: int,
    feedback_texto: str = "",
    dados_resposta: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Envia feedback/avaliação para o endpoint de feedback do assistente de IA
    
    Args:
        solicitacao_id: ID da solicitação original da IA
        avaliacao: Avaliação de 1-5 estrelas
        feedback_texto: Comentário opcional do usuário
        dados_resposta: Dados da resposta original para contexto
    
    Returns:
        Dict com resultado do envio do feedback
    """
    
    # URL do endpoint de feedback
    FEEDBACK_URL = f"http://localhost:8001/solicitacoes/{solicitacao_id}/feedback"
    
    # Preparar payload do feedback
    payload = {
        "avaliacao_usuario": avaliacao,
        "feedback_texto": feedback_texto,
        "usuario_satisfeito": avaliacao >= 4,  # 4-5 estrelas = satisfeito
        "resolveu_problema": avaliacao >= 3,   # 3+ estrelas = resolveu
        "precisou_escalacao": avaliacao <= 2,  # 1-2 estrelas = precisa escalação
        "timestamp_feedback": datetime.now().isoformat(),
        "origem_feedback": "mock_erp_dashboard"
    }
    
    # Adicionar contexto se disponível
    if dados_resposta:
        payload["contexto_original"] = {
            "request_id": dados_resposta.get("request", {}).get("requestId"),
            "categoria": dados_resposta.get("result", {}).get("categoria"),
            "tokens_used": dados_resposta.get("result", {}).get("tokens_used"),
            "response_time": dados_resposta.get("result", {}).get("response_time")
        }
    
    try:
        print(f"📤 Enviando feedback para IA: {payload}")
        
        # Fazer requisição PUT para o endpoint de feedback
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.put(
                FEEDBACK_URL,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "MockERP/1.0",
                    "X-Request-Source": "mock_erp_feedback"
                }
            )
            
            if response.status_code in [200, 201, 204]:
                resposta_feedback = response.json() if response.content else {}
                print(f"📥 Feedback enviado com sucesso: {resposta_feedback}")
                
                return {
                    "success": True,
                    "message": "Feedback enviado com sucesso",
                    "feedback_id": resposta_feedback.get("id"),
                    "status_code": response.status_code,
                    "response": resposta_feedback
                }
            
            else:
                # Erro na resposta da IA
                print(f"❌ Erro ao enviar feedback: Status {response.status_code}")
                print(f"📄 Resposta: {response.text}")
                error_msg = f"Erro ao enviar feedback: {response.status_code} - {response.text}"
                
                return {
                    "success": False,
                    "error": error_msg,
                    "status_code": response.status_code,
                    "fallback_message": "Feedback salvo localmente"
                }
    
    except httpx.TimeoutException:
        print(f"⏰ Timeout ao enviar feedback para IA")
        return {
            "success": False,
            "error": "Timeout na conexão com o serviço de feedback",
            "fallback_message": "Feedback salvo localmente"
        }
    
    except httpx.ConnectError:
        print(f"🔌 Erro de conexão ao enviar feedback para {FEEDBACK_URL}")
        return {
            "success": False,
            "error": "Serviço de feedback indisponível",
            "fallback_message": "Feedback salvo localmente"
        }
    
    except Exception as e:
        print(f"❌ Erro inesperado ao enviar feedback: {str(e)}")
        return {
            "success": False,
            "error": f"Erro inesperado: {str(e)}",
            "fallback_message": "Feedback salvo localmente"
        }
