"""
Serviço de E-mail para notificações de processamento de documentos
"""
import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv
import base64

load_dotenv()

logger = logging.getLogger(__name__)

class EmailService:
    """Serviço para envio de e-mails de notificação"""
    
    def __init__(self):
        """Inicializa o serviço de e-mail"""
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.email_from = os.getenv('EMAIL_FROM')
        self.email_to = os.getenv('EMAIL_TO', 'luan.amorim@fecaf.com.br')
        
        # Verifica se as configurações estão presentes
        if not all([self.smtp_username, self.smtp_password, self.email_from]):
            logger.warning("⚠️ Configurações de e-mail incompletas. E-mails não serão enviados.")
    
    def _create_html_template(self, dados_processados: Dict, documentos_info: List[Dict]) -> str:
        """Cria o template HTML do e-mail"""
        
        # Carrega a logo local como base64
        logo_path = os.path.join(os.path.dirname(__file__), '../../frontend/assets/logo_branco.png')
        logo_base64 = ""
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as img_file:
                logo_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        logo_img_tag = f'<img src="data:image/png;base64,{logo_base64}" alt="Logo UniFECAF" style="height: 60px; margin-bottom: 10px;" />' if logo_base64 else ""

        # Cria tabela com dados extraídos
        dados_html = ""
        if dados_processados:
            dados_html = """
            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                <thead>
                    <tr style="background-color: #242149; color: white;">
                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Campo</th>
                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Valor</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            for campo, valor in dados_processados.items():
                dados_html += f"""
                    <tr style="border-bottom: 1px solid #ddd;">
                        <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">{campo.replace('_', ' ').title()}</td>
                        <td style="padding: 12px; border: 1px solid #ddd;">{valor}</td>
                    </tr>
                """
            
            dados_html += """
                </tbody>
            </table>
            """
        
        # Cria lista de documentos processados
        docs_html = ""
        if documentos_info:
            docs_html = """
            <h3 style="color: #242149; margin-top: 30px;">📄 Documentos Processados</h3>
            <ul style="list-style: none; padding: 0;">
            """
            
            for doc in documentos_info:
                docs_html += f"""
                <li style="margin: 10px 0; padding: 10px; background-color: #f8f9fa; border-left: 4px solid #0E77CC;">
                    <strong>{doc.get('tipo', 'Documento')}:</strong> {doc.get('nome', 'N/A')}
                </li>
                """
            
            docs_html += "</ul>"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background: linear-gradient(135deg, #242149 0%, #1A3666 100%); color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .footer {{ background-color: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; color: #666; }}
                .success {{ color: #17A460; font-weight: bold; }}
                .info {{ color: #0E77CC; }}
            </style>
        </head>
        <body>
            <div class="header">
                {logo_img_tag}
                <h1>UniFECAF</h1>
                <p>Processamento Inteligente de Documentos</p>
            </div>
            
            <div class="content">
                <h2 class="success">✅ Documentos Processados com Sucesso!</h2>
                
                <p class="info">
                    <strong>Data/Hora:</strong> {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
                </p>
                
                <p>Os seguintes documentos foram processados e analisados pelo sistema de IA:</p>
                
                {docs_html}
                
                {dados_html}
                
                <div style="margin-top: 30px; padding: 15px; background-color: #e8f5e8; border-left: 4px solid #17A460;">
                    <p><strong>Status:</strong> Processamento concluído com sucesso</p>
                    <p><strong>IA Utilizada:</strong> OpenAI Vision API</p>
                </div>
            </div>
            
            <div class="footer">
                <p>Este e-mail foi gerado automaticamente pelo Sistema de Onboarding Inteligente UniFECAF</p>
                <p>© 2025 UniFECAF. Todos os direitos reservados.</p>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def _create_text_template(self, dados_processados: Dict, documentos_info: List[Dict]) -> str:
        """Cria o template de texto do e-mail"""
        
        text_content = f"""
🎓 UniFECAF - Processamento Inteligente de Documentos
{'='*60}

✅ DOCUMENTOS PROCESSADOS COM SUCESSO!

Data/Hora: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}

📄 DOCUMENTOS PROCESSADOS:
"""
        
        for doc in documentos_info:
            text_content += f"- {doc.get('tipo', 'Documento')}: {doc.get('nome', 'N/A')}\n"
        
        if dados_processados:
            text_content += "\n📋 DADOS EXTRAÍDOS:\n"
            for campo, valor in dados_processados.items():
                text_content += f"- {campo.replace('_', ' ').title()}: {valor}\n"
        
        text_content += f"""

Status: Processamento concluído com sucesso
IA Utilizada: OpenAI Vision API

{'='*60}
Este e-mail foi gerado automaticamente pelo Sistema de Onboarding Inteligente UniFECAF
© 2025 UniFECAF. Todos os direitos reservados.
"""
        
        return text_content
    
    def send_processing_notification(self, dados_processados: Dict, documentos_info: List[Dict], 
                                   process_id: Optional[str] = None) -> bool:
        """
        Envia e-mail de notificação de processamento
        
        Args:
            dados_processados: Dicionário com dados extraídos
            documentos_info: Lista com informações dos documentos
            process_id: ID do processo (opcional)
        
        Returns:
            bool: True se enviado com sucesso, False caso contrário
        """
        try:
            # Verifica se as configurações estão presentes
            if not all([self.smtp_username, self.smtp_password, self.email_from]):
                logger.warning("⚠️ Configurações de e-mail incompletas. E-mail não enviado.")
                return False
            
            # Cria o e-mail
            msg = MIMEMultipart('alternative')
            
            # Cria o subject de forma segura
            subject = f"✅ Documentos Processados - UniFECAF ({datetime.now().strftime('%d/%m/%Y')})"
            if process_id:
                subject += f" - ID: {process_id}"
            
            msg['Subject'] = subject
            msg['From'] = self.email_from
            msg['To'] = self.email_to
            
            # Cria versões HTML e texto
            html_content = self._create_html_template(dados_processados, documentos_info)
            text_content = self._create_text_template(dados_processados, documentos_info)
            
            # Anexa as versões
            msg.attach(MIMEText(text_content, 'plain', 'utf-8'))
            msg.attach(MIMEText(html_content, 'html', 'utf-8'))
            
            # Envia o e-mail
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"📧 E-mail de notificação enviado para {self.email_to}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao enviar e-mail: {str(e)}")
            return False
    
    def send_error_notification(self, error_message: str, documentos_info: List[Dict] = None) -> bool:
        """
        Envia e-mail de notificação de erro
        
        Args:
            error_message: Mensagem de erro
            documentos_info: Lista com informações dos documentos (opcional)
        
        Returns:
            bool: True se enviado com sucesso, False caso contrário
        """
        try:
            # Verifica se as configurações estão presentes
            if not all([self.smtp_username, self.smtp_password, self.email_from]):
                logger.warning("⚠️ Configurações de e-mail incompletas. E-mail não enviado.")
                return False
            
            # Cria o e-mail de erro
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"❌ Erro no Processamento - UniFECAF ({datetime.now().strftime('%d/%m/%Y')})"
            msg['From'] = self.email_from
            msg['To'] = self.email_to
            
            # Template de erro
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .header {{ background: linear-gradient(135deg, #242149 0%, #1A3666 100%); color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; }}
                    .error {{ color: #DC3545; font-weight: bold; }}
                    .footer {{ background-color: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; color: #666; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <img src="https://www.unifecaf.com.br/wp-content/uploads/2023/03/logo-unifecaf-branco.png" alt="UniFECAF" class="logo-img">
                    <p>Processamento Inteligente de Documentos</p>
                </div>
                
                <div class="content">
                    <h2 class="error">❌ Erro no Processamento</h2>
                    
                    <p><strong>Data/Hora:</strong> {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
                    
                    <div style="margin: 20px 0; padding: 15px; background-color: #ffeaea; border-left: 4px solid #DC3545;">
                        <p><strong>Erro:</strong> {error_message}</p>
                    </div>
                    
                    <p>O sistema encontrou um erro durante o processamento dos documentos.</p>
                </div>
                
                <div class="footer">
                    <p>Este e-mail foi gerado automaticamente pelo Sistema de Onboarding Inteligente UniFECAF</p>
                    <p>© 2025 UniFECAF. Todos os direitos reservados.</p>
                </div>
            </body>
            </html>
            """
            
            text_content = f"""
🎓 UniFECAF - Processamento Inteligente de Documentos
{'='*60}

❌ ERRO NO PROCESSAMENTO

Data/Hora: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}

Erro: {error_message}

O sistema encontrou um erro durante o processamento dos documentos.

{'='*60}
Este e-mail foi gerado automaticamente pelo Sistema de Onboarding Inteligente UniFECAF
© 2025 UniFECAF. Todos os direitos reservados.
"""
            
            # Anexa as versões
            msg.attach(MIMEText(text_content, 'plain', 'utf-8'))
            msg.attach(MIMEText(html_content, 'html', 'utf-8'))
            
            # Envia o e-mail
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"📧 E-mail de erro enviado para {self.email_to}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao enviar e-mail de erro: {str(e)}")
            return False 