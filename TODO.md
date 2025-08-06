# TODO - Mock ERP Teste Master Assistant

## 🔥 Próximas Funcionalidades

### Assistente Virtual
- [ ] Criar endpoint `/api/virtual-assistant` para receber dados do frontend
- [ ] Integrar com API de IA externa (ChatGPT, Claude, etc.)
- [ ] Implementar resposta inteligente no dialog
- [ ] Adicionar histórico de conversas

### Backend
- [ ] Adicionar banco de dados para persistência
- [ ] Implementar autenticação de usuários
- [ ] Criar endpoints CRUD para produtos
- [ ] Adicionar validações avançadas

### Frontend
- [ ] Melhorar responsividade mobile
- [ ] Adicionar loading states
- [ ] Implementar notificações toast
- [ ] Criar dashboard com gráficos

### Infraestrutura
- [ ] Configurar Docker
- [ ] Implementar testes automatizados
- [ ] Configurar CI/CD
- [ ] Deploy em produção

## 📝 Notas de Desenvolvimento

- FastAPI configurado com lifespan events (não usar @app.on_event deprecated)
- Frontend com 6 categorias de produtos implementadas
- Assistente virtual coleta dados do formulário automaticamente
- CORS configurado para desenvolvimento

## 🐛 Bugs Conhecidos

- Nenhum bug conhecido no momento

## 💡 Ideias Futuras

- Integração com WhatsApp Business API
- Relatórios em PDF
- Sistema de notificações por email
- Multi-idiomas (i18n)
