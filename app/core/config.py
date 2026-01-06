from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Reason: Na Vercel, se essas env vars não estiverem setadas, não podemos quebrar o boot.
    # Vamos validar sob demanda (nos endpoints/serviços que usam Bling).
    BLING_CLIENT_ID: str = ""
    BLING_CLIENT_SECRET: str = ""
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
    # Observação: Por enquanto não estamos criptografando os tokens; isso será aplicado na próxima etapa.
    ENCRYPTION_KEY: str = ""
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()


def assert_bling_oauth_configured() -> None:
    """
    Garante que as credenciais OAuth do Bling estão configuradas.

    Raises:
        RuntimeError: Se as credenciais não estiverem definidas via env vars.
    """
    if not settings.BLING_CLIENT_ID or not settings.BLING_CLIENT_SECRET:
        raise RuntimeError(
            "Configuração ausente: defina BLING_CLIENT_ID e BLING_CLIENT_SECRET nas Environment Variables da Vercel."
        )

