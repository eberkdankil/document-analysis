from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Configurar o diretório estático
app.static_folder = '.'
app.static_url_path = ''

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    print("🚀 Servidor Frontend iniciado!")
    print("📱 Acesse: http://localhost:5001")
    print("🔗 Backend rodando em: http://localhost:5000")
    print("⚠️  Certifique-se de que o backend está rodando!")
    app.run(host='0.0.0.0', port=5001, debug=True) 