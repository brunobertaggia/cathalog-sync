from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    BLING_CLIENT_ID: str
    BLING_CLIENT_SECRET: str
    REDIRECT_URI: str = "https://cathalog-sync-n31khw0rm-brunos-projects-f0960c16.vercel.app/auth/callback"
    DATABASE_URL: str = "sqlite:///./database.db"
    
    # Chave para criptografia de tokens sensíveis (AES)
    # Reason: Segurança extra para tokens armazenados no banco.
    ENCRYPTION_KEY: str = "32-byte-base64-encoded-key-here"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

