from fastapi import APIRouter, Query, HTTPException
import httpx
from app.core.config import settings
from app.core.database import engine
from app.models.auth import BlingToken
from sqlmodel import Session, select

@router.get("/callback")
async def auth_callback(code: str = Query(...)):
    """
    Endpoint de callback para o Bling OAuth 2.0.
    Troca o 'code' por 'access_token' e 'refresh_token'.
    """
    token_url = "https://www.bling.com.br/Api/v3/oauth/token"
    
    # Prepara o header de Basic Auth (client_id:client_secret em base64)
    auth_str = f"{settings.BLING_CLIENT_ID}:{settings.BLING_CLIENT_SECRET}"
    auth_b64 = base64.b64encode(auth_str.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {auth_b64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "authorization_code",
        "code": code
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data, headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=400, 
                detail=f"Erro ao trocar token no Bling: {response.text}"
            )
        
        token_data = response.json()
        
        # Salva o token no banco de dados
        with Session(engine) as session:
            # Remove tokens antigos para manter apenas o mais recente (simplificação inicial)
            old_tokens = session.exec(select(BlingToken)).all()
            for old in old_tokens:
                session.delete(old)
            
            new_token = BlingToken(
                access_token=token_data["access_token"],
                refresh_token=token_data["refresh_token"],
                expires_at=datetime.utcnow() + timedelta(seconds=token_data["expires_in"]),
                scope=token_data["scope"]
            )
            session.add(new_token)
            session.commit()
            
    return {"status": "success", "message": "Autenticação concluída com sucesso"}

@router.get("/login-url")
def get_login_url():
    """
    Retorna a URL que o usuário deve acessar para autorizar o app.
    """
    # Exemplo simplificado, o ideal é gerar um state único.
    state = "random_state_here"
    base_url = "https://www.bling.com.br/Api/v3/oauth/authorize"
    url = f"{base_url}?response_type=code&client_id={settings.BLING_CLIENT_ID}&state={state}"
    return {"url": url}

