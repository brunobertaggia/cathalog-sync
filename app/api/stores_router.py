from fastapi import APIRouter, HTTPException
from app.services.bling_client import BlingClient

router = APIRouter()
bling_client = BlingClient()

@router.get("/list")
async def list_stores():
    """
    Lista todas as lojas integradas no Bling para pegar os store_ids.
    """
    try:
        stores = await bling_client.get_stores()
        return {"stores": stores}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

