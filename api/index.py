from app.main import app

# Reason: Vercel espera funções Python dentro da pasta `api/`.
# Exportar `app` aqui torna o deploy mais estável para ASGI (FastAPI).


