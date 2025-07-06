# 🎓 Onboarding Inteligente de Documentos UniFECAF

Sistema completo para processamento inteligente de documentos (RG e Comprovante de Residência) usando OpenAI Vision, Supabase, e-mail e frontend responsivo.

---

## 🚀 Tecnologias Utilizadas

- **Backend:** Flask, Supabase (PostgreSQL), OpenAI Vision, SMTP (e-mail)
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
- Chave da API OpenAI (com acesso à Vision API)
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

**O arquivo `.env` deve estar dentro da pasta `backend/`!**

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

1. **Copie o `.env` para `backend/.env`** e configure com seus dados.
2. **No terminal, execute:**
   ```bash
   cd docker
   docker-compose up --build
   ```
3. **Acesse:**
   - Backend: [http://localhost:5000](http://localhost:5000)
   - Frontend: [http://localhost:5001](http://localhost:5001)

---

## 🔌 Endpoints Principais

- `POST /api/process-documents-base64` — Processa documentos (envio em base64)

---

## 📝 Observações Finais

- O sistema é totalmente containerizado: basta rodar o Docker Compose.
- O `.env` **deve estar em `backend/`** para o backend funcionar no container.
- O banco de dados Supabase deve ser criado conforme o SQL acima.
- O frontend e backend se comunicam localmente via API REST.

---

## 🎨 Identidade Visual UniFECAF

### Cores
- **Roxo:** #242149
- **Azul Escuro:** #1A3666
- **Azul Claro:** #0E77CC
- **Verde Escuro:** #17A460
- **Verde Claro:** #33DB89

### Tipografia
- **Fonte Principal:** Montserrat
- **Estilo:** Moderno, amigável e focado em clareza

## 📋 Pré-requisitos

- Python 3.8+
- Conta no Supabase
- Chave da API OpenAI (com acesso à Vision API)
- Conta de e-mail para SMTP

## 🔌 Endpoints da API

### Processamento de Documentos
- `POST /api/process-documents-base64` - Processa documentos em base64


### Testes e Monitoramento
- `GET /health` - Health check do sistema


## 🛠️ Instalação

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd "Teste Estudo de caso"
```

### 2. Configure o ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências
```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
```bash
# Copie o arquivo de exemplo
cp env.example .env

# Edite o arquivo .env com suas configurações
```

### 5. OpenAI Vision API
A OpenAI Vision API será usada para análise inteligente de documentos. Não requer instalação de bibliotecas OCR adicionais.

### 6. Configuração de E-mail
Configure as variáveis de ambiente para envio de notificações por e-mail:

**Para Gmail:**
1. Ative a verificação em 2 etapas
2. Gere uma "Senha de App" em Configurações > Segurança
3. Use essa senha no `SMTP_PASSWORD`

**Para Outlook/Hotmail:**
- Use `smtp-mail.outlook.com` como servidor
- Porta 587
- Use sua senha normal

## ⚙️ Configuração

### Variáveis de Ambiente (.env)

```env
# Flask
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True

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
EMAIL_TO=thiago.lopez@fecaf.com.br
```

## 🚀 Executando o Projeto

### 🔧 Execução Manual

#### 1. Backend
```bash
cd backend
python app.py
```
O servidor estará disponível em `http://localhost:5000`

#### 2. Frontend
```bash
cd frontend
python server.py
```
O frontend estará disponível em `http://localhost:5001`

### 📱 Outras Opções de Frontend

#### Opção 1: Servidor HTTP Simples
```bash
cd frontend
python -m http.server 3000
# Acesse: http://localhost:3000
```

#### Opção 2: Abrir Diretamente
Navegue até `frontend/index.html` e abra no navegador


### 🔧 Configurando Funções do Supabase

#### Aplicar Funções Manualmente
1. Acesse o painel do Supabase
2. Vá para **SQL Editor**
3. Copie e cole o conteúdo do arquivo `supabase_functions.sql`
4. Execute o script
5. Verifique se as funções foram criadas em **Database > Functions**


#### Teste Manual

1. **Inicie o backend:**
```bash
cd backend
python app.py
```

2. **Inicie o frontend:**
```bash
cd frontend
python server.py
```

3. **Acesse o sistema:**
- Frontend: http://localhost:5001
- Backend: http://localhost:5000

4. **Teste o upload:**
- Faça upload dos documentos (RG frente, RG verso, comprovante)
- Clique em "Processar Documentos"
- Veja os resultados extraídos

### Docker (Em desenvolvimento)
```bash
docker-compose up --build
```

## 📊 Estrutura do Banco de Dados

### Tabela: `documentos_processados`
- ID Processo (UUID)
- Tipo Documento
- Dados extraídos (Nome, CPF, RG, etc.)
- Status Processamento
- Dados brutos da OpenAI Vision
- Resposta da IA (JSON)

### Tabela: `logs_sistema`
- Logs de processamento
- Rastreamento de erros
- Auditoria do sistema

## 🔧 API Endpoints

### Principais Endpoints
- `GET /health` - Health check
- `POST /api/process-documents-base64` - Processa documentos em base64 (recomendado)
- `POST /api/process-documents` - Processa documentos via FormData (legado)
- `GET /api/test` - Teste da API
- `POST /api/test-upload` - Teste de upload de arquivos

## 📝 Funcionalidades

### Frontend - Interface de Upload
- **Design Responsivo** - Funciona em desktop, tablet e mobile
- **Drag & Drop** - Arraste arquivos diretamente para upload
- **Preview de Imagens** - Visualização dos arquivos selecionados
- **Validação em Tempo Real** - Verifica tipo e tamanho dos arquivos
- **Feedback Visual** - Status de upload e processamento
- **Identidade Visual UniFECAF** - Cores e design da instituição

### Backend - Processamento de Documentos
1. **Upload** - Interface para envio de documentos
2. **OpenAI** - Análise inteligente de imagens e extração de dados
3. **Validação** - Verificação de dados extraídos
4. **Armazenamento** - Salvamento no Supabase
5. **E-mail** - Notificação automática de sucesso/erro

### 📧 Serviço de E-mail
- **Notificação de Sucesso** - E-mail com dados extraídos e resumo
- **Notificação de Erro** - E-mail informando problemas no processamento
- **Template HTML** - E-mails formatados com identidade visual UniFECAF
- **Versão Texto** - Compatibilidade com clientes de e-mail simples
- **Configuração SMTP** - Suporte a Gmail, Outlook e outros provedores

### Tipos de Documentos Suportados
- RG (Frente e Verso)
- Comprovante de Residência (foto)
- Formatos: JPG, PNG


## 📞 Contato

- **E-mail:** luan.amorim@fecaf.com.br
- **Projeto:** Sistema de Onboarding Inteligente UniFECAF

---

**Status do Projeto:** 🟡 Em desenvolvimento
**Versão:** 1.0.0
**Última atualização:** Julho 2025