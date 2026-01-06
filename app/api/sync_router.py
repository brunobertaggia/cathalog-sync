from fastapi import APIRouter, Query
from app.services.sync_service import SyncService

router = APIRouter()
sync_service = SyncService()

@router.post("/categories")
async def sync_categories(dry_run: bool = Query(True)):
    """
    Sincroniza as categorias internas com o Bling.
    Use dry_run=True (padrão) para simular as criações.
    """
    results = await sync_service.sync_categories(dry_run=dry_run)
    return {"results": results, "dry_run": dry_run}

