# Dockerfile para o backend Flask UniFECAF
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Copia requirements e instala dependências
COPY ../backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do backend
COPY ../backend/ ./

# Expõe a porta padrão do Flask
EXPOSE 5000

# Variáveis de ambiente para produção
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Comando para rodar o backend
CMD ["flask", "run"] 