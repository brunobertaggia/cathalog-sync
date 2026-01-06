# Cathalog Sync

Serviço de sincronização de catálogo para Bling ERP (API v3).

## Como iniciar

### 1. Configurar Git
Para conectar este projeto ao seu repositório:
```bash
git init
git add .
git commit -m "Initial commit: Foundation and OAuth flow"
git branch -M main
git remote add origin <URL_DO_SEU_REPO_NO_GITHUB>
git push -u origin main
```

### 2. Configurar Ambiente
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Crie um arquivo `.env` na raiz com os dados que te passei:
   ```env
   BLING_CLIENT_ID=ba413352eb142d7ad449a79389e450a67b38f330
   BLING_CLIENT_SECRET=cc799fbc2d6ffa30c87944dd94885a041e42e31974f6c5fd66f94981a686
   REDIRECT_URI=https://cathalog-sync-n31khw0rm-brunos-projects-f0960c16.vercel.app/auth/callback
   ```

### 3. Rodar Localmente
```bash
uvicorn app.main:app --reload
```

## Fluxo de Autenticação
1. O app já está configurado para salvar tokens no `database.db`.
2. Como o app já foi autorizado na conta Bling, basta que o callback receba o `code` para gerar os tokens iniciais.
3. Se precisar de uma nova autorização, acesse `/auth/login-url` para pegar o link.

