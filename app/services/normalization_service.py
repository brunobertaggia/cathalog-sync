from sqlmodel import Session, select
from app.core.config import settings
from app.core.database import engine
from app.models.catalog import Category, AttributeRequirement

class NormalizationService:
    """
    Motor de Normalização.
    Responsável por aplicar a Fonte da Verdade aos produtos do Bling.
    """

    def __init__(self):
        self.bling_client = BlingClient()

    async def apply_category_to_product(self, sku: str, internal_category_id: int, dry_run: bool = True) -> Dict[str, Any]:
        """
        Vincula um produto a uma categoria e preenche atributos obrigatórios.
        """
        with Session(engine) as session:
            # 1. Buscar categoria interna
            category = session.get(Category, internal_category_id)
            if not category or not category.bling_id:
                return {"sku": sku, "status": "error", "message": "Categoria interna não sincronizada com Bling"}

            # 2. Buscar requisitos de atributos
            attributes = session.exec(
                select(AttributeRequirement).where(AttributeRequirement.category_id == internal_category_id)
            ).all()

            # 3. Buscar ID do produto no Bling pelo SKU
            # (Simplificado: buscando na lista de produtos. Em produção, buscaríamos por SKU diretamente se a API permitir)
            all_products = await self.bling_client.get_products(limit=100)
            product = next((p for p in all_products if p.get("codigo") == sku), None)

            if not product:
                return {"sku": sku, "status": "error", "message": "Produto não encontrado no Bling"}

            product_id = product.get("id")

            # 4. Preparar dados para atualização
            update_data = {
                "categoria": {"id": int(category.bling_id)},
                # Aqui poderíamos adicionar campos customizados/atributos se a API v3 permitir via patch direto
                # Por enquanto focamos na categoria que é o maior gargalo.
            }

            if dry_run:
                return {
                    "sku": sku, 
                    "status": "dry_run_pending", 
                    "new_category": category.name,
                    "bling_category_id": category.bling_id
                }

            # 5. Executar atualização
            try:
                await self.bling_client.update_product(product_id, update_data)
                return {"sku": sku, "status": "success", "category": category.name}
            except Exception as e:
                return {"sku": sku, "status": "error", "message": str(e)}

    async def batch_normalize(self, skus: List[str], internal_category_id: int, dry_run: bool = True) -> List[Dict[str, Any]]:
        """Aplica normalização em massa para uma lista de SKUs."""
        results = []
        for sku in skus:
            res = await self.apply_category_to_product(sku, internal_category_id, dry_run)
            results.append(res)
        return results

