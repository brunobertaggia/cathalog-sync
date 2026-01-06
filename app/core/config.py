from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    BLING_CLIENT_ID: str
    BLING_CLIENT_SECRET: str
    REDIRECT_URI: str = "https://cathalog-sync-n31khw0rm-brunos-projects-f0960c16.vercel.app/auth/callback"
    # No Vercel, o SQLite só funciona na pasta /tmp
    DATABASE_URL: str = "sqlite:////tmp/database.db"
    
    # Ajuste automático para strings do Supabase/Heroku se necessário
    @property
    def sqlalchemy_database_url(self) -> str:
        if self.DATABASE_URL.startswith("postgres://"):
            return self.DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
        return self.DATABASE_URL
    
    # Chave para criptografia de tokens sensíveis (AES)
    # Reason: Segurança extra para tokens armazenados no banco.
    ENCRYPTION_KEY: str = "32-byte-base64-encoded-key-here"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

