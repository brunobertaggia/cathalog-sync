import anthropic
import json
import re
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

    @staticmethod
    def _extract_json_object(text: str) -> Dict[str, Any]:
        """
        Extrai o primeiro objeto JSON encontrado no texto.

        Reason: Modelos às vezes retornam texto extra mesmo quando pedimos "apenas JSON".
        """
        # Match guloso mínimo do primeiro {...}
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            return {}
        try:
            return json.loads(match.group(0))
        except Exception:
            return {}

    async def enrich_product_data(self, product_title: str, product_description: str, required_attributes: List[str]) -> Dict[str, Any]:
        """
        Analisa o produto e extrai os valores para os atributos solicitados.
        """
        prompt = f"""
Você é um especialista em cadastro de produtos para marketplaces.

Tarefa: preencher os atributos abaixo, baseado APENAS no título e descrição do produto.

TÍTULO:
{product_title}

DESCRIÇÃO:
{product_description}

ATRIBUTOS (use exatamente esses nomes como chaves do JSON):
{json.dumps(required_attributes, ensure_ascii=False)}

Regras:
- Responda com um ÚNICO objeto JSON (sem markdown, sem texto fora do JSON)
- As chaves devem ser exatamente os nomes dos atributos listados
- Se não for possível inferir com segurança, use "N/A"

Exemplo de resposta (formato):
{{"Marca":"Clink","Material":"Bambu","Capacidade":"N/A"}}
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
            parsed = self._extract_json_object(content)
            # Garantir que todos os atributos existam no retorno
            return {attr: parsed.get(attr, "N/A") for attr in required_attributes}
        except Exception as e:
            # Em caso de erro, retorna os atributos como N/A para não travar o processo
            return {attr: "N/A" for attr in required_attributes}

