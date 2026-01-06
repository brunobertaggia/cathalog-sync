# Workflow State

## Log
- [2026-01-06] Inicialização do projeto.
- [2026-01-06] Criação do PLANNING.md com a arquitetura e tech stack.

## Plan
### Fase 1: Fundação e Autenticação
1. **Configuração Inicial**:
   - Criar estrutura de pastas (`app/`, `tests/`, `alembic/`).
   - Configurar `requirements.txt` ou `pyproject.toml`.
   - Definir modelos de banco de dados para `BlingToken`.
2. **Implementação OAuth 2.0**:
   - Criar endpoint de callback para receber o `code` do Bling.
   - Implementar troca de `code` por `access_token` e `refresh_token`.
   - Criar serviço de refresh automático de token.
3. **Cliente API Bling**:
   - Implementar wrapper básico para chamadas GET (Categorias, Produtos).

### Fase 2: Auditoria e Fonte da Verdade
1. **Script de Auditoria**:
   - Buscar todas as categorias atuais do Bling.
   - Buscar produtos e mapear estados atuais.
2. **Modelagem Interna**:
   - Definir tabelas para Categorias Canônicas e Mapeamentos de Marketplace.

### Fase 3: Sincronização
1. **Sync de Categorias**:
   - Lógica para criar categorias no Bling baseada na fonte da verdade.
2. **Normalização**:
   - Aplicar categorias e atributos aos produtos.

## Status
State.Status = CONSTRUCT

