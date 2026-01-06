from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class BlingToken(SQLModel, table=True):
    """
    Representa o token de acesso OAuth 2.0 do Bling.
    Reason: Armazena o estado da autenticação para renovação automática.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    access_token: str
    refresh_token: str
    expires_at: datetime
    scope: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

