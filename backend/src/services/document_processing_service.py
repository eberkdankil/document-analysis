"""
Serviço integrado para processamento de documentos
"""
import os
import logging
import tempfile
import uuid
import base64
from datetime import datetime
from typing import Dict, List, Optional, Any
from ..models.documento_processado import DocumentoProcessado
from ..models.log_sistema import LogSistema
from .openai_vision_service import OpenAIVisionService
from .supabase_service import SupabaseService
from .email_service import EmailService

logger = logging.getLogger(__name__)

class DocumentProcessingService:
    """
    Serviço integrado para processamento completo de documentos
    """
    
    def __init__(self):
        """Inicializa o serviço de processamento"""
        self.vision_service = OpenAIVisionService()
        self.supabase_service = SupabaseService()
        self.email_service = EmailService()
    
    def process_documents_base64(self, 
                                rg_frente_data: Dict,
                                rg_verso_data: Dict,
                                comprovante_data: Dict,
                                email_contato: Optional[str] = None) -> Dict[str, Any]:
        """
        Processa documentos em base64 de forma completa
        
        Args:
            rg_frente_data: Dados do RG frente (base64, filename, etc)
            rg_verso_data: Dados do RG verso (base64, filename, etc)
            comprovante_data: Dados do comprovante (base64, filename, etc)
            email_contato: Email de contato (opcional)
            
        Returns:
            Dict com resultado do processamento
        """
        session_id = str(uuid.uuid4())
        temp_dir = None
        
        try:
            logger.info(f"🔄 Iniciando processamento completo - Session ID: {session_id}")
            
            # Cria diretório temporário
            temp_dir = tempfile.mkdtemp()
            
            # Salva arquivos temporários
            rg_frente_path = os.path.join(temp_dir, f"{session_id}_rg_frente.jpg")
            rg_verso_path = os.path.join(temp_dir, f"{session_id}_rg_verso.jpg")
            comprovante_path = os.path.join(temp_dir, f"{session_id}_comprovante.jpg")
            
            # Decodifica e salva arquivos
            self._save_base64_file(rg_frente_data['base64'], rg_frente_path)
            self._save_base64_file(rg_verso_data['base64'], rg_verso_path)
            self._save_base64_file(comprovante_data['base64'], comprovante_path)
            
            logger.info("📁 Arquivos temporários salvos")
            
            # Processa com OpenAI Vision
            logger.info("🤖 Iniciando análise com OpenAI Vision...")
            vision_result = self.vision_service.analisar_documentos(
                rg_frente_path=rg_frente_path,
                rg_verso_path=rg_verso_path,
                comprovante_path=comprovante_path
            )
            
            if not vision_result.get('success'):
                logger.error(f"❌ Erro na análise da OpenAI: {vision_result.get('error')}")
                return self._handle_processing_error(
                    session_id, vision_result.get('error', 'Erro desconhecido'),
                    [rg_frente_data, rg_verso_data, comprovante_data]
                )
            
            # Extrai dados da resposta da OpenAI
            dados_extraidos = vision_result.get('dados_extraidos', {})
            ia_response = vision_result.get('dados_ia_response', {})
            
            logger.info("✅ Análise da OpenAI concluída com sucesso")
            
            # Salva no banco de dados
            logger.info("💾 Salvando dados no banco...")
            db_result = self._save_to_database(
                session_id=session_id,
                dados_extraidos=dados_extraidos,
                ia_response=ia_response,
                documentos_info=[
                    {'tipo': 'RG - Frente', 'nome': rg_frente_data.get('filename', 'RG Frente')},
                    {'tipo': 'RG - Verso', 'nome': rg_verso_data.get('filename', 'RG Verso')},
                    {'tipo': 'Comprovante de Residência', 'nome': comprovante_data.get('filename', 'Comprovante')}
                ],
                email_contato=email_contato
            )
            
            if not db_result.get('success'):
                logger.error(f"❌ Erro ao salvar no banco: {db_result.get('error')}")
                return self._handle_processing_error(
                    session_id, db_result.get('error', 'Erro ao salvar no banco'),
                    [rg_frente_data, rg_verso_data, comprovante_data]
                )
            
            logger.info("✅ Dados salvos no banco com sucesso")
            
            # Envia e-mail de notificação
            logger.info("📧 Enviando e-mail de notificação...")
            email_sent = self.email_service.send_processing_notification(
                dados_processados=dados_extraidos,
                documentos_info=[
                    {'tipo': 'RG - Frente', 'nome': rg_frente_data.get('filename', 'RG Frente')},
                    {'tipo': 'RG - Verso', 'nome': rg_verso_data.get('filename', 'RG Verso')},
                    {'tipo': 'Comprovante de Residência', 'nome': comprovante_data.get('filename', 'Comprovante')}
                ],
                process_id=session_id
            )
            
            if email_sent:
                logger.info("✅ E-mail enviado com sucesso")
            else:
                logger.warning("⚠️ E-mail não foi enviado")
            
            # Limpa arquivos temporários
            self._cleanup_temp_files(temp_dir, [rg_frente_path, rg_verso_path, comprovante_path])
            
            # Cria log de sucesso SOMENTE se o documento foi salvo com sucesso
            if db_result.get('success') and db_result.get('id_processo'):
                self._create_success_log(
                    db_result['id_processo'],
                    "Processamento concluído com sucesso",
                    dados_extraidos=dados_extraidos,
                    documentos_info=[
                        {'tipo': 'RG - Frente', 'nome': rg_frente_data.get('filename', 'RG Frente')},
                        {'tipo': 'RG - Verso', 'nome': rg_verso_data.get('filename', 'RG Verso')},
                        {'tipo': 'Comprovante de Residência', 'nome': comprovante_data.get('filename', 'Comprovante')}
                    ],
                    email_contato=email_contato,
                    modelo_ia=vision_result.get('modelo_utilizado')
                )

            logger.info(f"🎉 Processamento completo finalizado - Session ID: {session_id}")
            
            return {
                'success': True,
                'message': 'Documentos processados com sucesso!',
                'session_id': session_id,
                'data': dados_extraidos,
                'modelo_utilizado': vision_result.get('modelo_utilizado'),
                'arquivos_analisados': vision_result.get('arquivos_analisados_count', 0),
                'email_enviado': email_sent,
                'banco_salvo': True,
                'timestamp': str(datetime.now())
            }
            
        except Exception as e:
            logger.error(f"❌ Erro no processamento: {str(e)}")
            return self._handle_processing_error(
                session_id, str(e),
                [rg_frente_data, rg_verso_data, comprovante_data]
            )
        finally:
            # Garante limpeza dos arquivos temporários
            if temp_dir:
                self._cleanup_temp_files(temp_dir, [rg_frente_path, rg_verso_path, comprovante_path])
    
    def _save_base64_file(self, base64_data: str, file_path: str):
        """Salva arquivo base64 no caminho especificado"""
        try:
            with open(file_path, 'wb') as f:
                f.write(base64.b64decode(base64_data))
            logger.info(f"✅ Arquivo salvo: {file_path}")
        except Exception as e:
            logger.error(f"❌ Erro ao salvar arquivo {file_path}: {str(e)}")
            raise
    
    def _save_to_database(self, 
                          session_id: str,
                          dados_extraidos: Dict,
                          ia_response: Dict,
                          documentos_info: List[Dict],
                          email_contato: Optional[str] = None) -> Dict[str, Any]:
        """
        Salva dados processados no banco de dados (apenas um registro unificado)
        """
        try:
            # Converte data de emissão para formato ISO se necessário
            data_emissao = dados_extraidos.get('data_emissao')
            if data_emissao:
                data_emissao = self._convert_date_to_iso(data_emissao)

            # Preenche campos de endereço vindos do comprovante
            endereco = dados_extraidos.get('endereco_completo') or dados_extraidos.get('endereco')
            cidade = dados_extraidos.get('cidade')
            estado = dados_extraidos.get('estado')
            cep = dados_extraidos.get('cep')

            # Cria documento processado unificado
            documento = DocumentoProcessado(
                tipo_documento='PROCESSAMENTO_UNIFICADO',
                nome_completo=dados_extraidos.get('nome_completo'),
                cpf=dados_extraidos.get('cpf'),
                rg=dados_extraidos.get('rg'),
                data_emissao_rg=data_emissao,
                endereco=endereco,
                cidade=cidade,
                estado=estado,
                cep=cep,
                email_contato=email_contato,
                arquivo_original_nome=f"RG: {documentos_info[0].get('nome', 'Frente')} + {documentos_info[1].get('nome', 'Verso')} | Comprovante: {documentos_info[2].get('nome', 'Comprovante')}",
                dados_ia_response=ia_response
            )

            # Salva no banco
            db_result = self.supabase_service.inserir_documento(documento)
            logger.info(f"✅ Documento unificado salvo no banco: {db_result.get('id_processo', 'N/A')}")

            return {
                'success': True,
                'id_processo': db_result.get('id_processo'),
            }
        except Exception as e:
            logger.error(f"❌ Erro ao salvar no banco: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _handle_processing_error(self, 
                                session_id: str,
                                error_message: str,
                                documentos_info: List[Dict]) -> Dict[str, Any]:
        """
        Trata erros no processamento
        """
        try:
            # Cria log de erro
            self._create_error_log(session_id, error_message)
            
            # Envia e-mail de erro
            try:
                self.email_service.send_error_notification(
                    error_message=error_message,
                    documentos_info=[
                        {'tipo': 'RG - Frente', 'nome': documentos_info[0].get('filename', 'RG Frente')},
                        {'tipo': 'RG - Verso', 'nome': documentos_info[1].get('filename', 'RG Verso')},
                        {'tipo': 'Comprovante de Residência', 'nome': documentos_info[2].get('filename', 'Comprovante')}
                    ]
                )
                logger.info("📧 E-mail de erro enviado")
            except Exception as email_error:
                logger.error(f"❌ Erro ao enviar e-mail de erro: {str(email_error)}")
            
            return {
                'success': False,
                'error': error_message,
                'session_id': session_id,
                'message': 'Erro no processamento dos documentos',
                'timestamp': str(datetime.now())
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao tratar erro: {str(e)}")
            return {
                'success': False,
                'error': f"Erro no processamento: {error_message}",
                'session_id': session_id,
                'message': 'Erro interno do servidor',
                'timestamp': str(datetime.now())
            }
    
    def _create_success_log(self, session_id: str, message: str, dados_extraidos=None, documentos_info=None, email_contato=None, modelo_ia=None):
        """Cria log de sucesso com detalhes do processamento"""
        try:
            detalhes = {
                "dados_extraidos": dados_extraidos or {},
                "arquivos": [info['nome'] for info in documentos_info] if documentos_info else [],
                "email_contato": email_contato,
                "modelo_ia": modelo_ia,
                "timestamp": str(datetime.now())
            }
            log = LogSistema(
                id_processo=session_id,
                tipo_log='SUCCESS',
                mensagem=message,
                nivel='INFO',
                detalhes=detalhes
            )
            self.supabase_service.inserir_log(log)
        except Exception as e:
            logger.error(f"❌ Erro ao criar log de sucesso: {str(e)}")
    
    def _create_error_log(self, session_id: str, error_message: str, dados_recebidos=None):
        """Cria log de erro com detalhes do erro"""
        try:
            import traceback
            detalhes = {
                "erro": str(error_message),
                "dados_recebidos": dados_recebidos or {},
                "stacktrace": traceback.format_exc(),
                "timestamp": str(datetime.now())
            }
            log = LogSistema(
                id_processo=session_id,
                tipo_log='ERROR',
                mensagem="Erro ao processar documentos",
                nivel='ERROR',
                detalhes=detalhes
            )
            self.supabase_service.inserir_log(log)
        except Exception as e:
            logger.error(f"❌ Erro ao criar log de erro: {str(e)}")
    
    def _convert_date_to_iso(self, date_str: str) -> str:
        """
        Converte data do formato brasileiro (dd/mm/yyyy) para ISO (yyyy-mm-dd)
        
        Args:
            date_str: Data no formato dd/mm/yyyy
            
        Returns:
            str: Data no formato yyyy-mm-dd ou string original se não conseguir converter
        """
        try:
            if not date_str or '/' not in date_str:
                return date_str
            
            # Tenta converter dd/mm/yyyy para yyyy-mm-dd
            parts = date_str.split('/')
            if len(parts) == 3:
                day, month, year = parts
                # Garante que o ano tem 4 dígitos
                if len(year) == 2:
                    year = '20' + year
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            
            return date_str
        except Exception as e:
            logger.warning(f"⚠️ Erro ao converter data '{date_str}': {str(e)}")
            return date_str
    
    def _cleanup_temp_files(self, temp_dir: str, file_paths: List[str]):
        """Limpa arquivos temporários"""
        try:
            for file_path in file_paths:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info(f"🧹 Arquivo removido: {file_path}")
            
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
                logger.info(f"🧹 Diretório temporário removido: {temp_dir}")
                
        except Exception as e:
            logger.warning(f"⚠️ Erro ao limpar arquivos temporários: {str(e)}")
    
    def get_processing_status(self, session_id: str) -> Dict[str, Any]:
        """
        Obtém status do processamento
        
        Args:
            session_id: ID da sessão de processamento
            
        Returns:
            Dict com status do processamento
        """
        try:
            # Busca documentos no banco
            documentos = self.supabase_service.listar_documentos()
            documentos_session = [doc for doc in documentos if doc.get('id_processo') == session_id]
            
            # Busca logs
            logs = self.supabase_service.listar_logs(id_processo=session_id)
            
            return {
                'success': True,
                'session_id': session_id,
                'documentos_encontrados': len(documentos_session),
                'logs_encontrados': len(logs),
                'documentos': documentos_session,
                'logs': logs
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar status: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'session_id': session_id
            } 