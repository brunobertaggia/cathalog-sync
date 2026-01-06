from sqlmodel import Session, select
from app.core.database import engine
from app.models.catalog import Category, CategoryMapping
from app.services.bling_client import BlingClient
from typing import List, Optional

class SyncService:
    """
    Motor de Sincronização.
    Responsável por garantir que a Fonte da Verdade (DB) seja refletida no Bling.
    """
    
    def __init__(self):
        self.bling_client = BlingClient()

    async def sync_categories(self, dry_run: bool = True) -> List[dict]:
        """
        Sincroniza a árvore de categorias e SEUS VÍNCULOS MULTILOJA com o Bling.
        """
        sync_log = []
        
        with Session(engine) as session:
            # 1. Buscar todas as categorias internas
            categories = session.exec(select(Category)).all()
            categories_sorted = sorted(categories, key=lambda x: (x.parent_id is not None, x.id))

            for cat in categories_sorted:
                # A. Garantir que a categoria existe no Bling
                if not cat.bling_id:
                    if dry_run:
                        sync_log.append({"name": cat.name, "status": "dry_run_pending_creation"})
                    else:
                        parent_bling_id = None
                        if cat.parent_id:
                            parent_cat = session.get(Category, cat.parent_id)
                            parent_bling_id = parent_cat.bling_id if parent_cat else None

                        try:
                            bling_data = await self.bling_client.create_category(cat.name, parent_bling_id)
                            cat.bling_id = str(bling_data.get("id"))
                            session.add(cat)
                            session.commit()
                            sync_log.append({"name": cat.name, "status": "created", "bling_id": cat.bling_id})
                        except Exception as e:
                            sync_log.append({"name": cat.name, "status": "error", "message": str(e)})
                            continue # Pula vínculos se a criação falhou
                else:
                    sync_log.append({"name": cat.name, "status": "already_exists", "bling_id": cat.bling_id})

                # B. Processar Vínculos Multiloja para esta categoria
                mappings = session.exec(select(CategoryMapping).where(CategoryMapping.category_id == cat.id)).all()
                for mapping in mappings:
                    if dry_run:
                        sync_log.append({
                            "category": cat.name,
                            "marketplace": mapping.marketplace_name,
                            "status": "dry_run_pending_link",
                            "external_id": mapping.external_category_id
                        })
                    else:
                        try:
                            await self.bling_client.link_category_to_store(
                                category_id=cat.bling_id,
                                store_id=mapping.bling_store_id,
                                external_category_id=mapping.external_category_id
                            )
                            sync_log.append({
                                "category": cat.name,
                                "marketplace": mapping.marketplace_name,
                                "status": "linked_success"
                            })
                        except Exception as e:
                            sync_log.append({
                                "category": cat.name,
                                "marketplace": mapping.marketplace_name,
                                "status": "link_error",
                                "message": str(e)
                            })

        return sync_log

