from sqlmodel import Session, select, create_engine
from app.core.config import settings
from app.models.catalog import Category
from app.services.bling_client import BlingClient
from typing import List, Optional

engine = create_engine(settings.DATABASE_URL)

class SyncService:
    """
    Motor de Sincronização.
    Responsável por garantir que a Fonte da Verdade (DB) seja refletida no Bling.
    """
    
    def __init__(self):
        self.bling_client = BlingClient()

    async def sync_categories(self, dry_run: bool = True) -> List[dict]:
        """
        Sincroniza a árvore de categorias com o Bling.
        Se a categoria não existe no Bling (bling_id is None), ela é criada.
        """
        sync_log = []
        
        with Session(engine) as session:
            # 1. Buscar todas as categorias internas, ordenadas por nível (pais primeiro)
            # Para simplificar, buscamos todas. Em escala, usaríamos recursividade ou níveis.
            categories = session.exec(select(Category)).all()
            
            # Ordenar categorias para garantir que pais sejam criados antes dos filhos
            # (categorias sem parent_id primeiro)
            categories_sorted = sorted(categories, key=lambda x: (x.parent_id is not None, x.id))

            for cat in categories_sorted:
                if cat.bling_id:
                    sync_log.append({"name": cat.name, "status": "already_synced", "bling_id": cat.bling_id})
                    continue

                if dry_run:
                    sync_log.append({"name": cat.name, "status": "dry_run_pending_creation"})
                    continue

                # Criar no Bling
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

        return sync_log

