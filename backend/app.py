"""
Aplicação Flask básica para testar a configuração inicial
"""
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Cria e configura a aplicação Flask"""
    app = Flask(__name__)
    
    # Configura CORS para permitir requisições do frontend
    CORS(app)
    
    # Rota de teste básica
    @app.route('/')
    def index():
        """Página inicial"""
        return jsonify({
            'message': '🎓 Sistema de Onboarding Inteligente UniFECAF',
            'status': 'online',
            'version': '1.0.0'
        })
    
    # Rota de health check
    @app.route('/health')
    def health():
        """Verifica se a aplicação está funcionando"""
        return jsonify({
            'status': 'healthy',
            'message': 'Sistema funcionando corretamente!'
        })
    
    # Rota principal de processamento
    @app.route('/api/process-documents-base64', methods=['POST'])
    def process_documents_base64():
        try:
            data = request.get_json()
            if not data:
                return jsonify({'success': False, 'error': 'Dados JSON não fornecidos'}), 400
            required_fields = ['rg_frente', 'rg_verso', 'comprovante']
            for field in required_fields:
                if field not in data:
                    return jsonify({'success': False, 'error': f'Campo obrigatório não encontrado: {field}'}), 400
            from src.services.document_processing_service import DocumentProcessingService
            processing_service = DocumentProcessingService()
            email_contato = data.get('email_contato')
            resultado = processing_service.process_documents_base64(
                rg_frente_data=data['rg_frente'],
                rg_verso_data=data['rg_verso'],
                comprovante_data=data['comprovante'],
                email_contato=email_contato
            )
            if resultado.get('success'):
                return jsonify(resultado)
            else:
                return jsonify(resultado), 500
        except Exception as e:
            return jsonify({'success': False, 'error': str(e), 'message': 'Erro interno do servidor'}), 500
    
    # Log quando a aplicação inicia
    logger.info("🚀 Aplicação Flask configurada com sucesso!")
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    print("🎓 Sistema de Onboarding Inteligente UniFECAF")
    print("=" * 50)
    print("🚀 Iniciando servidor...")
    print("📱 Acesse: http://localhost:5000")
    print("🔍 Health check: http://localhost:5000/health")
    print("=" * 50)
    
    # Executa a aplicação
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
