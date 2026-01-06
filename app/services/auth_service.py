import httpx
from datetime import datetime, timedelta
from sqlmodel import Session, select, create_engine
from app.core.config import settings
from app.models.auth import BlingToken
import base64

engine = create_engine(settings.DATABASE_URL)

class AuthService:
    """
    Serviço para gerenciar a autenticação e renovação de tokens.
    """
    
    @staticmethod
    async def get_valid_token() -> str:
        """
        Retorna um access_token válido. 
        Se o atual estiver expirado, renova automaticamente usando o refresh_token.
        """
        with Session(engine) as session:
            statement = select(BlingToken).order_by(BlingToken.created_at.desc())
            token = session.exec(statement).first()
            
            if not token:
                raise Exception("Nenhum token encontrado. Por favor, autentique primeiro.")
            
            # Margem de segurança de 1 minuto
            if datetime.utcnow() + timedelta(minutes=1) < token.expires_at:
                return token.access_token
            
            # Token expirado ou próximo de expirar: renovar
            return await AuthService.refresh_access_token(token)

    @staticmethod
    async def refresh_access_token(token_obj: BlingToken) -> str:
        """
        Executa o fluxo de refresh token com o Bling.
        """
        token_url = "https://www.bling.com.br/Api/v3/oauth/token"
        auth_str = f"{settings.BLING_CLIENT_ID}:{settings.BLING_CLIENT_SECRET}"
        auth_b64 = base64.b64encode(auth_str.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {auth_b64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "refresh_token",
            "refresh_token": token_obj.refresh_token
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=data, headers=headers)
            
            if response.status_code != 200:
                raise Exception(f"Erro ao renovar token: {response.text}")
            
            new_data = response.json()
            
            with Session(engine) as session:
                token_obj.access_token = new_data["access_token"]
                token_obj.refresh_token = new_data["refresh_token"]
                token_obj.expires_at = datetime.utcnow() + timedelta(seconds=new_data["expires_in"])
                token_obj.updated_at = datetime.utcnow()
                
                session.add(token_obj)
                session.commit()
                session.refresh(token_obj)
                
                return token_obj.access_token

