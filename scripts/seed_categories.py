from sqlmodel import Session, create_engine, SQLModel
from app.core.config import settings
from app.models.catalog import Category, AttributeRequirement
from app.models.auth import BlingToken # Importante para criar todas as tabelas

engine = create_engine(settings.sqlalchemy_database_url)

def create_tables():
    """Garante que todas as tabelas sejam criadas no banco local."""
    SQLModel.metadata.create_all(engine)

def seed_initial_categories():
    """
    Popula o banco com categorias iniciais e requisitos de atributos.
    """
    create_tables()
    with Session(engine) as session:
        # 1. Criar Categorias
        cat_cozinha = Category(name="Utilidades Domésticas > Cozinha")
        cat_brinquedos = Category(name="Brinquedos > Educativos")
        
        session.add(cat_cozinha)
        session.add(cat_brinquedos)
        session.commit()
        session.refresh(cat_cozinha)
        session.refresh(cat_brinquedos)
        
        # 2. Criar Requisitos de Atributos (Campos que os Marketplaces pedem)
        attrs = [
            # Atributos OBRIGATÓRIOS para Mercado Livre em Cozinha
            AttributeRequirement(category_id=cat_cozinha.id, marketplace_id="mercado_livre", attribute_name="Marca"),
            AttributeRequirement(category_id=cat_cozinha.id, marketplace_id="mercado_livre", attribute_name="Modelo"),
            AttributeRequirement(category_id=cat_cozinha.id, marketplace_id="mercado_livre", attribute_name="Material"),
            
            # Atributos OBRIGATÓRIOS para Mercado Livre em Brinquedos
            AttributeRequirement(category_id=cat_brinquedos.id, marketplace_id="mercado_livre", attribute_name="Marca"),
            AttributeRequirement(category_id=cat_brinquedos.id, marketplace_id="mercado_livre", attribute_name="Modelo"),
            AttributeRequirement(category_id=cat_brinquedos.id, marketplace_id="mercado_livre", attribute_name="Idade mínima recomendada"),
        ]
        
        for attr in attrs:
            session.add(attr)
        
        session.commit()
        print("Categorias e Atributos iniciais inseridos com sucesso!")

if __name__ == "__main__":
    seed_initial_categories()

