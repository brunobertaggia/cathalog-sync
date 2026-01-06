from sqlmodel import Session, select
from app.core.database import engine
from app.models.catalog import Category, AttributeRequirement
from app.services.bling_client import BlingClient
from app.services.claude_service import ClaudeService
from typing import List, Dict, Any

class NormalizationService:
    """
    Motor de Normalização.
    Responsável por aplicar a Fonte da Verdade aos produtos do Bling.
    """

    def __init__(self):
        self.bling_client = BlingClient()
        self.claude_service = ClaudeService()

    async def apply_category_to_product(self, sku: str, internal_category_id: int, dry_run: bool = True, use_ai: bool = True) -> Dict[str, Any]:
        """
        Vincula um produto a uma categoria e preenche atributos obrigatórios usando IA.
        """
        with Session(engine) as session:
            # 1. Buscar categoria interna
            category = session.get(Category, internal_category_id)
            if not category or not category.bling_id:
                return {"sku": sku, "status": "error", "message": "Categoria interna não sincronizada com Bling"}

            # 2. Buscar requisitos de atributos (campos customizados/características)
            attribute_reqs = session.exec(
                select(AttributeRequirement).where(AttributeRequirement.category_id == internal_category_id)
            ).all()

            # 3. Buscar o produto no Bling
            all_products = await self.bling_client.get_products(limit=100)
            product = next((p for p in all_products if p.get("codigo") == sku), None)

            if not product:
                return {"sku": sku, "status": "error", "message": "Produto não encontrado no Bling"}

            product_id = product.get("id")
            
            # 4. Inteligência: Preencher atributos via Claude se habilitado
            enriched_attributes = []
            ai_details = {}
            
            if use_ai and attribute_reqs:
                required_names = [req.attribute_name for req in attribute_reqs]
                # Busca detalhes completos do produto para a IA analisar
                full_product = await self.bling_client.get_product_by_id(product_id)
                
                ai_results = await self.claude_service.enrich_product_data(
                    product_title=full_product.get("nome", ""),
                    product_description=full_product.get("descricaoCurta", ""),
                    required_attributes=required_names
                )
                
                for req in attribute_reqs:
                    val = ai_results.get(req.attribute_name, req.default_value or "N/A")
                    enriched_attributes.append({
                        "nome": req.attribute_name,
                        "valor": val
                    })
                    ai_details[req.attribute_name] = val

            # 5. Preparar dados para atualização
            update_data = {
                "categoria": {"id": int(category.bling_id)},
            }
            
            if enriched_attributes:
                # No Bling v3, 'caracteristicas' é o campo para atributos de produto
                update_data["caracteristicas"] = enriched_attributes

            if dry_run:
                return {
                    "sku": sku, 
                    "status": "dry_run_pending", 
                    "new_category": category.name,
                    "suggested_attributes": ai_details
                }

            # 6. Executar atualização real
            try:
                await self.bling_client.update_product(product_id, update_data)
                return {
                    "sku": sku, 
                    "status": "success", 
                    "category": category.name,
                    "attributes_updated": list(ai_details.keys())
                }
            except Exception as e:
                return {"sku": sku, "status": "error", "message": str(e)}

    async def batch_normalize(self, skus: List[str], internal_category_id: int, dry_run: bool = True, use_ai: bool = True) -> List[Dict[str, Any]]:
        """Aplica normalização em massa para uma lista de SKUs."""
        results = []
        for sku in skus:
            res = await self.apply_category_to_product(sku, internal_category_id, dry_run, use_ai)
            results.append(res)
        return results

