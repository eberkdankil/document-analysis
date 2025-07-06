# 🎓 Onboarding Inteligente de Documentos UniFECAF

Sistema completo para processamento inteligente de documentos (RG e Comprovante de Residência) usando OpenAI, Supabase, e-mail e frontend responsivo.

---

## 🚀 Tecnologias Utilizadas

- **Backend:** Flask, Supabase (PostgreSQL), OpenAI, SMTP (e-mail)
- **Frontend:** HTML, CSS, JS (servidor Python simples)
- **DevOps:** Docker, Docker Compose

---

## 📁 Estrutura do Projeto

```
Teste Estudo de caso/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── .env
│   └── src/
│       ├── models/
│       ├── services/
│       └── ...
│
├── frontend/
│   ├── index.html
│   ├── server.py
│   ├── assets/
│   ├── css/
│   └── js/
│
└── docker/
    ├── Dockerfile
    ├── Dockerfile.frontend
    ├── docker-compose.yml
    └── .dockerignore
```

---

## ⚙️ Pré-requisitos

- Docker e Docker Compose instalados
- Conta no Supabase (PostgreSQL)
- Chave da API OpenAI (modelos com leitura de imagens, ex: gpt-4o-mini)
- Conta de e-mail SMTP (para notificações)

---

## 🛠️ Configuração do Banco de Dados (Supabase)

Crie as tabelas com o seguinte SQL:

```sql
CREATE TABLE public.documentos_processados (
  id integer NOT NULL DEFAULT nextval('documentos_processados_id_seq'::regclass),
  id_processo uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE,
  tipo_documento character varying NOT NULL,
  nome_completo character varying,
  cpf character varying,
  rg character varying,
  data_emissao_rg date,
  endereco text,
  cidade character varying,
  estado character varying,
  cep character varying,
  status_processamento character varying,
  data_processamento timestamp without time zone DEFAULT now(),
  observacoes text,
  email_contato character varying,
  arquivo_original_nome character varying,
  dados_ia_response jsonb,
  created_at timestamp without time zone DEFAULT now(),
  updated_at timestamp without time zone DEFAULT now(),
  CONSTRAINT documentos_processados_pkey PRIMARY KEY (id)
);

CREATE TABLE public.logs_sistema (
  id integer NOT NULL DEFAULT nextval('logs_sistema_id_seq'::regclass),
  id_processo uuid,
  nivel character varying NOT NULL,
  mensagem text NOT NULL,
  detalhes jsonb,
  timestamp timestamp without time zone DEFAULT now(),
  tipo_log text,
  CONSTRAINT logs_sistema_pkey PRIMARY KEY (id),
  CONSTRAINT logs_sistema_id_processo_fkey FOREIGN KEY (id_processo) REFERENCES public.documentos_processados(id_processo)
);
```

---

## 🔑 Variáveis de Ambiente

O arquivo `.env` deve estar dentro da pasta `backend/`!

Exemplo de `.env`:

```env
# Flask
FLASK_APP=app.py
FLASK_ENV=production

# Supabase
SUPABASE_URL=sua_url_do_supabase
SUPABASE_KEY=sua_chave_do_supabase

# OpenAI
OPENAI_API_KEY=sua_chave_da_openai

# E-mail
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=seu_email@gmail.com
SMTP_PASSWORD=sua_senha_de_app
EMAIL_FROM=seu_email@gmail.com
EMAIL_TO=destinatario@dominio.com
```

---

## 🐳 Como Subir Tudo com Docker

1. Copie o `.env` para `backend/.env` e configure com seus dados.
2. No terminal, execute:
   ```bash
   cd docker
   docker-compose up --build
   ```
3. Acesse:
   - Backend: [http://localhost:5000](http://localhost:5000)
   - Frontend: [http://localhost:5001](http://localhost:5001)

---

## 🔌 Endpoints da API

- `POST /api/process-documents-base64` — Processa documentos (envio em base64)
- `GET /health` — Health check do sistema

---

## 📝 Funcionalidades

### Frontend
- Design responsivo (desktop, tablet, mobile)
- Drag & Drop e preview de imagens
- Validação em tempo real e feedback visual
- Identidade visual UniFECAF

### Backend
- Processamento inteligente com OpenAI
- Validação e salvamento no Supabase
- Notificação automática por e-mail (sucesso/erro)
- Logs detalhados de processamento

### Tipos de Documentos Suportados
- RG (Frente e Verso)
- Comprovante de Residência (foto)
- Formatos: JPG, PNG

---

## 🎨 Identidade Visual UniFECAF

- **Roxo:** #242149
- **Azul Escuro:** #1A3666
- **Azul Claro:** #0E77CC
- **Verde Escuro:** #17A460
- **Verde Claro:** #33DB89
- **Fonte:** Montserrat

---

## 🛠️ Instalação Manual (sem Docker)

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd "Teste Estudo de caso"
   ```
2. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # ou
   source venv/bin/activate  # Linux/Mac
   ```
3. Instale as dependências:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
4. Configure o `.env` conforme exemplo acima.

5. Inicie o backend:
   ```bash
   python app.py
   ```
   O backend estará em `http://localhost:5000`

6. Inicie o frontend:
   ```bash
   cd frontend
   python server.py
   ```
   O frontend estará em `http://localhost:5001`

---

## 📞 Contato

- **E-mail:** luan.amorim@fecaf.com.br
- **Projeto:** Sistema de Onboarding Inteligente UniFECAF

---

**Status do Projeto:** 🟡 Em desenvolvimento  
**Versão:** 1.0.0  
**Última atualização:** Julho 2025
