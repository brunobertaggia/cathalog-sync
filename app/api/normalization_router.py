from fastapi import APIRouter, Query, Body
from app.services.normalization_service import NormalizationService
from app.services.audit_service import AuditService
from typing import List

router = APIRouter()
norm_service = NormalizationService()
audit_service = AuditService()

@router.post("/normalize-skus")
async def normalize_skus(
    skus: List[str] = Body(...), 
    category_id: int = Query(...), 
    dry_run: bool = Query(True),
    use_ai: bool = Query(True)
):
    """
    Normaliza uma lista de SKUs aplicando uma categoria específica e preenchendo atributos com IA.
    """
    results = await norm_service.batch_normalize(skus, category_id, dry_run, use_ai)
    return {"results": results, "dry_run": dry_run}

@router.post("/normalize-pending-skus")
async def normalize_pending_skus(
    category_id: int = Query(...), 
    dry_run: bool = Query(True),
    use_ai: bool = Query(True)
):
    """
    Pega automaticamente a lista de SKUs pendentes (da imagem) 
    e tenta normalizá-los com a categoria informada usando IA.
    """
    pending_skus = audit_service.load_pending_skus()
    results = await norm_service.batch_normalize(pending_skus, category_id, dry_run, use_ai)
    return {"results": results, "dry_run": dry_run}
