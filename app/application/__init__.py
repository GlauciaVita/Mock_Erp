"""
Módulo Application - Mock ERP
Contém a lógica de negócio da aplicação
"""

from .solicitacoes import (
    GerenciadorSolicitacoes,
    SolicitacaoBase,
    SolicitacaoAssistenteVirtual,
    SolicitacaoProduto,
    SolicitacaoSuporte,
    SolicitacaoCreate,
    criar_solicitacao_assistente_virtual,
    processar_solicitacao_assistente,
    gerar_resposta_simulada,
    enviar_para_assistente_ia,
    enviar_para_assistente_ia_sync,
    verificar_status_assistente_ia,
    detectar_categoria_solicitacao,
    detectar_subcategoria_solicitacao,
    extrair_palavras_chave,
    extrair_topicos_abordados,
    extrair_entidades,
    detectar_complexidade,
    detectar_sentimento,
    gerar_tags
)

__all__ = [
    "GerenciadorSolicitacoes",
    "SolicitacaoBase", 
    "SolicitacaoAssistenteVirtual",
    "SolicitacaoProduto",
    "SolicitacaoSuporte",
    "SolicitacaoCreate",
    "criar_solicitacao_assistente_virtual",
    "processar_solicitacao_assistente",
    "gerar_resposta_simulada",
    "enviar_para_assistente_ia",
    "enviar_para_assistente_ia_sync",
    "verificar_status_assistente_ia",
    "detectar_categoria_solicitacao",
    "detectar_subcategoria_solicitacao",
    "extrair_palavras_chave",
    "extrair_topicos_abordados",
    "extrair_entidades",
    "detectar_complexidade",
    "detectar_sentimento",
    "gerar_tags"
]
