from fastapi import APIRouter, HTTPException
from app.services.audit_service import AuditService

router = APIRouter()
audit_service = AuditService()

@router.get("/run")
async def run_audit():
    """
    Executa a auditoria de produtos e categorias.
    Foca especialmente nos SKUs que ainda não foram exportados.
    """
    try:
        results = await audit_service.run_audit()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

