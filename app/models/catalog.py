from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Category(SQLModel, table=True):
    """
    Categoria Canônica - A Fonte da Verdade.
    Reason: Define a estrutura hierárquica que deve ser replicada nos marketplaces.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    parent_id: Optional[int] = Field(default=None, foreign_key="category.id")
    
    # ID correspondente no Bling (para manter o vínculo após a criação)
    bling_id: Optional[str] = Field(default=None, index=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relacionamentos
    parent: Optional["Category"] = Relationship(back_populates="children", sa_relationship_kwargs={"remote_side": "Category.id"})
    children: List["Category"] = Relationship(back_populates="parent")
    mappings: List["CategoryMapping"] = Relationship(back_populates="category")

class CategoryMapping(SQLModel, table=True):
    """
    Mapeamento de Categoria por Marketplace.
    Reason: Cada canal (ML, Shopee, etc.) tem sua própria árvore de categorias.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    category_id: int = Field(foreign_key="category.id")
    marketplace_id: str = Field(index=True) # Ex: 'mercado_livre', 'shopee'
    external_category_id: str # ID da categoria no marketplace
    external_category_name: Optional[str] = None
    
    category: Category = Relationship(back_populates="mappings")

class AttributeRequirement(SQLModel, table=True):
    """
    Atributos Obrigatórios por Categoria/Marketplace.
    Reason: Automatiza o preenchimento de campos exigidos para exportação.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    category_id: int = Field(foreign_key="category.id")
    marketplace_id: str = Field(index=True)
    attribute_name: str
    is_required: bool = True
    default_value: Optional[str] = None

