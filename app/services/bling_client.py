import httpx
from typing import List, Dict, Any
from app.services.auth_service import AuthService

class BlingClient:
    """
    Cliente para interação com a API v3 do Bling.
    Reason: Centraliza todas as chamadas externas, facilitando manutenção e logs.
    """
    
    BASE_URL = "https://www.bling.com.br/Api/v3"

    async def _get(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        token = await AuthService.get_valid_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/{endpoint}", headers=headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                # Log de erro (futuramente via Logger, não console.log)
                raise Exception(f"Erro na API Bling ({endpoint}): {response.text}")

    async def get_categories(self) -> List[Dict[str, Any]]:
        """Busca todas as categorias cadastradas no Bling."""
        # A API v3 do Bling usa paginação. Implementação simplificada da primeira página.
        response = await self._get("categorias/produtos")
        return response.get("data", [])

    async def get_products(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Busca produtos do Bling."""
        response = await self._get("produtos", params={"limite": limit})
        return response.get("data", [])

    async def get_product_by_id(self, product_id: str) -> Dict[str, Any]:
        """Busca os detalhes de um produto específico."""
        response = await self._get(f"produtos/{product_id}")
        return response.get("data", {})

    async def update_product(self, product_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Atualiza um produto no Bling.
        """
        token = await AuthService.get_valid_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.patch(f"{self.BASE_URL}/produtos/{product_id}", json=data, headers=headers)
            if response.status_code in [200, 204]:
                return {"status": "success"}
            else:
                raise Exception(f"Erro ao atualizar produto no Bling: {response.text}")

    async def get_product_characteristics(self, product_id: str) -> List[Dict[str, Any]]:
        """Busca as características (atributos) de um produto."""
        # Na v3, características costumam estar dentro do nó 'caracteristicas' do produto
        product = await self.get_product_by_id(product_id)
        return product.get("caracteristicas", [])

    async def create_category(self, name: str, parent_id: str = None) -> Dict[str, Any]:
        """Cria uma nova categoria no Bling."""
        data = {"descricao": name}
        if parent_id:
            data["idCategoriaPai"] = parent_id
            
        token = await AuthService.get_valid_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.BASE_URL}/categorias/produtos", json=data, headers=headers)
            if response.status_code == 201:
                return response.json().get("data", {})
            else:
                raise Exception(f"Erro ao criar categoria no Bling: {response.text}")

