import anthropic
import json
from app.core.config import settings, assert_claude_configured
from typing import Dict, Any, List

class ClaudeService:
    """
    Serviço de Inteligência usando Claude (Anthropic).
    Reason: Analisa títulos e descrições para extrair atributos obrigatórios dos marketplaces.
    """

    def __init__(self):
        assert_claude_configured()
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def enrich_product_data(self, product_title: str, product_description: str, required_attributes: List[str]) -> Dict[str, Any]:
        """
        Analisa o produto e extrai os valores para os atributos solicitados.
        """
        prompt = f"""
        Você é um especialista em e-commerce e ERP Bling.
        Analise o seguinte produto e extraia os valores para os atributos listados.
        
        Produto: {product_title}
        Descrição: {product_description}
        
        Atributos Necessários: {', '.join(required_attributes)}
        
        Responda APENAS um JSON puro (sem markdown) no seguinte formato:
        {{
            "atributo_nome": "valor_extraido",
            "justificativa": "breve motivo"
        }}
        Se não encontrar um atributo, use "N/A".
        """

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extrair o conteúdo da resposta
            content = response.content[0].text
            return json.loads(content)
        except Exception as e:
            # Em caso de erro, retorna os atributos como N/A para não travar o processo
            return {attr: "N/A" for attr in required_attributes}

