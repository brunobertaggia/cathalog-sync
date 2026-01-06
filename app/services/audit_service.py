import json
import os
from typing import List, Dict, Any
from app.services.bling_client import BlingClient

class AuditService:
    """
    Serviço de Auditoria para mapear o estado atual do Bling.
    Reason: Identificar inconsistências e produtos que ainda não foram exportados.
    """

    def __init__(self):
        self.bling_client = BlingClient()
        self.pending_skus_path = "data/pending_skus.json"

    def load_pending_skus(self) -> List[str]:
        if os.path.exists(self.pending_skus_path):
            with open(self.pending_skus_path, 'r') as f:
                return json.load(f)
        return []

    async def run_audit(self) -> Dict[str, Any]:
        """
        Executa a auditoria completa.
        """
        pending_skus = self.load_pending_skus()
        
        # 1. Buscar produtos do Bling (usando paginação simples para auditoria inicial)
        # Nota: Em um cenário real com milhares de produtos, usaríamos um Job assíncrono.
        all_products = await self.bling_client.get_products(limit=100)
        
        audit_results = {
            "total_bling_products": len(all_products),
            "pending_skus_found_in_bling": [],
            "pending_skus_missing_in_bling": [],
            "products_without_category": [],
            "summary": {}
        }

        bling_skus = {p.get("codigo"): p for p in all_products if p.get("codigo")}

        # Verificar SKUs pendentes
        for sku in pending_skus:
            if sku in bling_skus:
                product = bling_skus[sku]
                audit_results["pending_skus_found_in_bling"].append({
                    "sku": sku,
                    "id": product.get("id"),
                    "nome": product.get("nome"),
                    "categoria": product.get("categoria", {}).get("nome", "SEM CATEGORIA")
                })
            else:
                audit_results["pending_skus_missing_in_bling"].append(sku)

        # Identificar produtos sem categoria no Bling
        for product in all_products:
            if not product.get("categoria"):
                audit_results["products_without_category"].append({
                    "sku": product.get("codigo"),
                    "nome": product.get("nome")
                })

        audit_results["summary"] = {
            "total_pending_requested": len(pending_skus),
            "found_pending": len(audit_results["pending_skus_found_in_bling"]),
            "missing_pending": len(audit_results["pending_skus_missing_in_bling"]),
            "total_without_category": len(audit_results["products_without_category"])
        }

        return audit_results

