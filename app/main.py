from fastapi import FastAPI
from app.api import auth_router, audit_router, sync_router, normalization_router
from app.core.config import settings
from app.core.database import engine
from sqlmodel import SQLModel

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(
    title="Cathalog Sync API",
    description="Sincronizador de catálogo com o Bling ERP",
    version="0.1.0"
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Registro de Rotas
app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
app.include_router(audit_router.router, prefix="/audit", tags=["Audit"])
app.include_router(sync_router.router, prefix="/sync", tags=["Sync"])
app.include_router(normalization_router.router, prefix="/normalization", tags=["Normalization"])

@app.get("/")
def read_root():
    return {"status": "online", "message": "Cathalog Sync is running"}

