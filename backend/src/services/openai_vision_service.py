"""
Serviço de integração com OpenAI Vision API
"""
import os
import base64
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from openai import OpenAI

logger = logging.getLogger(__name__)

class OpenAIVisionService:
    """
    Serviço para análise de documentos usando OpenAI Vision API
    """
    
    def __init__(self):
        # print("Iniciando OpenAIVisionService")
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        # print(f"API Key encontrada: {api_key[:10] if api_key and len(api_key) > 10 else 'NÃO ENCONTRADA'}...")
        if not api_key or api_key == 'sua_chave_da_openai':
            raise ValueError("OPENAI_API_KEY deve estar definido nas variáveis de ambiente! Verifique o arquivo .env")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
    
    def _encode_file_to_base64(self, file_path: str) -> str:
        """
        Codifica arquivo para base64
        
        Args:
            file_path (str): Caminho do arquivo
            
        Returns:
            str: Arquivo codificado em base64
        """
        try:
            with open(file_path, "rb") as file:
                return base64.b64encode(file.read()).decode('utf-8')
        except Exception as e:
            # logger.error(f"Erro ao codificar arquivo {file_path}: {str(e)}")
            raise
    
    def _clean_json_response(self, ai_response: str) -> str:
        """
        Remove blocos markdown da resposta da IA
        """
        cleaned = ai_response.strip()
        if cleaned.startswith('```json'):
            cleaned = cleaned[7:]
        if cleaned.startswith('```'):
            cleaned = cleaned[3:]
        if cleaned.endswith('```'):
            cleaned = cleaned[:-3]
        return cleaned.strip()

    def analisar_documentos(self, 
                           rg_frente_path: str = None,
                           rg_verso_path: str = None,
                           comprovante_path: str = None) -> Dict[str, Any]:
        """
        Analisa todos os documentos fornecidos usando base64
        
        Args:
            rg_frente_path (str): Caminho da imagem da frente do RG
            rg_verso_path (str): Caminho da imagem do verso do RG
            comprovante_path (str): Caminho do comprovante de residência
            
        Returns:
            Dict[str, Any]: Resultado da análise com todos os dados
        """
        try:
            # logger.info("Iniciando análise de documentos via base64")
            files_to_analyze = []
            if rg_frente_path and os.path.exists(rg_frente_path):
                files_to_analyze.append(("rg_frente", rg_frente_path))
                # logger.info(f"RG Frente adicionado: {rg_frente_path}")
            if rg_verso_path and os.path.exists(rg_verso_path):
                files_to_analyze.append(("rg_verso", rg_verso_path))
                # logger.info(f"RG Verso adicionado: {rg_verso_path}")
            if comprovante_path and os.path.exists(comprovante_path):
                files_to_analyze.append(("comprovante", comprovante_path))
                # logger.info(f"Comprovante adicionado: {comprovante_path}")
            if not files_to_analyze:
                raise ValueError("Nenhum arquivo válido fornecido para análise")
            prompt = self._create_prompt(rg_frente_path, rg_verso_path, comprovante_path)
            resultado = self._analyze_base64_files(files_to_analyze, prompt)
            resultado['arquivos_analisados'] = {
                'rg_frente': rg_frente_path if rg_frente_path and os.path.exists(rg_frente_path) else None,
                'rg_verso': rg_verso_path if rg_verso_path and os.path.exists(rg_verso_path) else None,
                'comprovante': comprovante_path if comprovante_path and os.path.exists(comprovante_path) else None
            }
            resultado['timestamp'] = str(datetime.now())
            # logger.info("Análise concluída com sucesso")
            return resultado
        except Exception as e:
            # logger.error(f"Erro na análise dos documentos: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': str(datetime.now())
            }

    def _create_prompt(self, rg_frente_path: str, rg_verso_path: str, comprovante_path: str) -> str:
        """
        Cria um prompt único para análise de RG (frente e verso) e comprovante de residência
        """
        return (
            """
            Analise as imagens anexadas (frente e verso do RG e comprovante de residência) e extraia TODOS os dados relevantes em um único JSON estruturado, conforme o exemplo abaixo:

            {
                "nome_completo": "Nome completo da pessoa",
                "rg": "Número do RG",
                "cpf": "CPF",
                "data_emissao": "Data de emissão do RG",
                "orgao_emissor": "Órgão emissor do RG",
                "uf_emissor": "UF do órgão emissor do RG",
                "nome_mae": "Nome da mãe",
                "nome_pai": "Nome do pai (se visível)",
                "data_nascimento": "Data de nascimento",
                "naturalidade": "Naturalidade",
                "uf_naturalidade": "UF da naturalidade",
                "endereco_completo": "Endereço completo do comprovante",
                "bairro": "Bairro",
                "cidade": "Cidade",
                "estado": "Estado (UF)",
                "cep": "CEP",
                "tipo_comprovante": "Tipo do comprovante (conta de luz, água, etc.)"
            }

            IMPORTANTE:
            - Retorne APENAS o JSON válido, sem explicações ou texto extra.
            - Se alguma informação não estiver visível, use null.
            - Mantenha a formatação exata do JSON.
            """
        )

    def _analyze_base64_files(self, files_to_analyze: List[tuple], prompt: str) -> Dict[str, Any]:
        """
        Analisa múltiplos arquivos usando base64
        """
        try:
            # logger.info(f"Analisando {len(files_to_analyze)} arquivos via base64")
            content = []
            for _, file_path in files_to_analyze:
                base64_image = self._encode_file_to_base64(file_path)
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                })
            content.append({
                "type": "text",
                "text": prompt
            })
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": content
                }],
                max_tokens=1500,
                temperature=0.1
            )
            ai_response = response.choices[0].message.content
            # logger.info(f"Resposta da IA recebida: {ai_response[:100]}...")
            try:
                cleaned_response = self._clean_json_response(ai_response)
                dados_extraidos = json.loads(cleaned_response)
            except json.JSONDecodeError as e:
                # logger.error(f"Erro ao fazer parse do JSON: {str(e)}")
                # logger.error(f"Resposta da IA: {ai_response}")
                raise ValueError(f"Resposta da IA não é um JSON válido: {str(e)}")
            return {
                'success': True,
                'dados_extraidos': dados_extraidos,
                'dados_ia_response': ai_response,
                'modelo_utilizado': self.model,
                'arquivos_analisados_count': len(files_to_analyze)
            }
        except Exception as e:
            # logger.error(f"Erro na análise base64: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
