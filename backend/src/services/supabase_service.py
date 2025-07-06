"""
Serviço de integração com o Supabase
"""
import os
from datetime import datetime
from supabase import create_client, Client
from typing import Optional, Dict, Any, List
from ..models.documento_processado import DocumentoProcessado
from ..models.log_sistema import LogSistema

class SupabaseService:
    """
    Serviço para integração com o banco de dados Supabase
    """
    def __init__(self):
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        if not url or not key:
            raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar definidos nas variáveis de ambiente!")
        self.client: Client = create_client(url, key)

    # Documentos
    def inserir_documento(self, documento: DocumentoProcessado) -> Dict[str, Any]:
        data = documento.to_dict()
        # Remove campos que não existem na tabela
        data.pop('id', None)
        data.pop('created_at', None)
        data.pop('updated_at', None)
        response = self.client.table('documentos_processados').insert(data).execute()
        return response.data[0] if response.data else {}

    # Logs
    def inserir_log(self, log: LogSistema) -> Dict[str, Any]:
        data = log.to_dict()
        data.pop('id', None)
        response = self.client.table('logs_sistema').insert(data).execute()
        return response.data[0] if response.data else {}