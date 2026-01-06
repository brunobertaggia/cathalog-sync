from sqlmodel import Session, create_engine
from app.core.config import settings
from app.models.catalog import Category

engine = create_engine(settings.DATABASE_URL)

def seed_initial_categories():
    """
    Popula o banco com categorias iniciais para teste.
    Edite esta lista conforme sua necessidade.
    """
    with Session(engine) as session:
        # Exemplo de estrutura
        cats = [
            Category(name="Eletrônicos"),
            Category(name="Acessórios Automotivos"),
            Category(name="Casa e Decoração"),
        ]
        
        for cat in cats:
            session.add(cat)
        
        session.commit()
        print("Categorias iniciais inseridas com sucesso!")

if __name__ == "__main__":
    seed_initial_categories()

