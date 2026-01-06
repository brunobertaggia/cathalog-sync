# Cathalog Sync - Planejamento do Projeto

## 1. Visão Geral
O **Cathalog Sync** é um serviço de backend projetado para ser a "fonte da verdade" para o catálogo de produtos do ERP Bling. Ele automatiza a gestão de categorias, vínculos multiloja e preenchimento de atributos, eliminando a necessidade de ajustes manuais no Bling.

## 2. Objetivos Principais
- **Sincronização de Categorias**: Garantir que a estrutura de categorias interna seja refletida no Bling.
- **Normalização de Produtos**: Categorizar e preencher atributos obrigatórios automaticamente.
- **Gestão de Marketplace**: Mapear categorias internas para as exigências específicas de cada marketplace (Mercado Livre, Shopee, etc.).
- **Automação OAuth 2.0**: Gerenciar tokens de acesso e refresh da API v3 do Bling.

## 3. Tech Stack
- **Linguagem**: Python 3.11+
- **Framework Web**: FastAPI
- **ORM/Banco de Dados**: SQLModel (SQLAlchemy + Pydantic) / PostgreSQL
- **Validação**: Pydantic v2
- **Requisições API**: HTTPX
- **Testes**: Pytest
- **Deploy**: Vercel (Backend + Database)

## 4. Arquitetura do Sistema
O projeto será dividido em módulos claros:
- `app/core/auth`: Gestão de tokens OAuth do Bling.
- `app/api/bling`: Cliente para comunicação com a API v3 do Bling.
- `app/services/sync`: Lógica de sincronização e regras de negócio.
- `app/models`: Definições de tabelas e esquemas de dados.
- `app/jobs`: Tarefas agendadas para sincronização automática.

## 5. Convenções e Padrões
- **Idempotência**: Todas as operações de sincronização devem poder ser executadas repetidamente sem causar duplicidade ou erros.
- **Dry-run**: Implementar um modo de simulação para prever alterações antes de aplicá-las.
- **Logs**: Logs detalhados de todas as alterações feitas no Bling (sem usar console.log, usando logging do Python).
- **Segurança**: Armazenamento seguro de segredos e tokens.

## 6. Roadmap Inicial
1. [x] Configuração do ambiente e estrutura base.
2. [x] Implementação do fluxo OAuth 2.0 (Callback + Refresh).
3. [x] Auditoria de categorias e produtos existentes no Bling.
4. [x] Definição da estrutura da "Fonte da Verdade".
5. [x] Sincronização automática de categorias.
6. [x] Automação de atributos e normalização de produtos.

