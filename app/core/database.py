from sqlmodel import create_engine
from app.core.config import settings

# Reason: Centraliza a criação do engine para facilitar a troca de banco (SQLite -> Postgres)
engine = create_engine(settings.sqlalchemy_database_url)

