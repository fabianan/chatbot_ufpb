# Assistente Institucional da UFPB

Este projeto implementa um chatbot com **RAG (Retrieval-Augmented Generation)** para auxiliar docentes, técnicos, estudantes e gestores da Universidade Federal da Paraíba (UFPB) na consulta a resoluções, editais, documentos normativos e bases de conhecimento internas.

A aplicação utiliza **modelos de linguagem generativa** integrados a um motor de **busca semântica vetorial (FAISS)** com dados extraídos de arquivos PDF e do sistema BookStack do STI/UFPB.

---

## Funcionalidades

- Interface via **Streamlit** com chat interativo
- Carregamento automático de resoluções e editais da UFPB em PDF
- Integração com BookStack para acesso a artigos e perguntas frequentes
- Vetorização com `sentence-transformers` e busca semântica com FAISS
- Encaminhamento por perfil/tema com base no conteúdo do `.json` de unidades
- Histórico de conversa com memória de contexto na sessão
- Reindexação manual da base vetorial (botão 🔁)

---

## Tecnologias Utilizadas

- **Python 3.11+**
- **Streamlit**
- **LangChain (community, huggingface)**
- **FAISS** para vetores
- **sentence-transformers** (HuggingFace)
- **BookStack API** (via tokens)
- **PDF Parsing com PyPDF2**
- **dotenv para variáveis de ambiente**

---

## ⚙️ Como Executar Localmente

### 1. Clone o repositório

```bash
git clone https://github.com/fabianan/chatbot_ufpb.git
cd chatbot_ufpb
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Crie um arquivo `.env` com suas chaves:

```env
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
HF_API_TOKEN=your_huggingface_token
BOOKSTACK_TOKEN_ID=your_bookstack_id
BOOKSTACK_TOKEN_SECRET=your_bookstack_secret
```

### 4. Rode o app

```bash
streamlit run app/main.py
```

---

## 📁 Estrutura de Diretórios

```
chatbot_ufpb/
├── app/
│   ├── main.py                # App principal do Streamlit
│   ├── loader.py              # Lê PDFs, BookStack e cria vetores FAISS
│   ├── rag.py                 # Define o pipeline RAG (retriever + model)
│   ├── memory.py              # Memória de conversa na sessão
│   ├── db.py                  # Carrega unidades institucionais e URLs
│   ├── utils.py               # Funções auxiliares de formatação
│   └── bookstack_loader.py    # Busca artigos no BookStack via API
├── data/
│   ├── base_conhecimento_url.txt     # Lista de URLs do BookStack
│   ├── unidades_negociais.json       # Lista de unidades com atribuições
│   └── pdfs/                          # PDFs baixados dos sites da UFPB
├── .streamlit/
│   └── secrets.toml          # Chaves de API em produção (para Streamlit Cloud)
├── .env                      # Chaves de API em ambiente local (não subir no GitHub)
├── requirements.txt
└── README.md
```

---

## 📄 Explicação dos Arquivos `.py`

### `main.py`

- Interface Streamlit principal
- Inicializa vetores, memória e cadeia RAG
- Exibe histórico da conversa e interface de chat
- Controla botão de reindexação de documentos e PDF sidebar

### `loader.py`

- Faz download de PDFs a partir de URLs
- Extrai texto com `PyPDFLoader`
- Usa `RecursiveCharacterTextSplitter` para dividir o texto
- Integra dados da BookStack
- Gera e carrega índice vetorial FAISS com embeddings HuggingFace

### `bookstack_loader.py`

- Usa `requests` e `BeautifulSoup` para extrair conteúdo HTML do BookStack
- Conecta via tokens API configurados no `.env`
- Lê URLs listadas no `base_conhecimento_url.txt`

### `db.py`

- Carrega arquivos de configuração de URLs e JSON de unidades institucionais
- Suporta classificação de responsabilidade por palavras-chave

### `rag.py`

- Define o pipeline RAG com LangChain
- Usa retriever (FAISS) + modelo LLM (via Gemini/OpenAI/HuggingFace)
- Usa prompt engineering e condicionamento baseado na unidade

### `memory.py`

- Controla histórico de conversas via `ConversationBufferMemory`
- Armazena mensagens trocadas entre usuário e assistente

### `utils.py`

- Funções de formatação, exibição e processamento auxiliar


---

## Sugestões de Perguntas

> “Sou aluno de pós-graduação, em que turmas devo me matricular para 2025.1?”

> “Como cadastrar uma eleição no sistema de eleições da UFPB?”

> “Qual setor trata de trancamento parcial?”

---

## Desenvolvedora

**Fabiana Ferreira do Nascimento**\
MBA em Ciência de Dados e Inteligência Artificial\
[github.com/fabianan](https://github.com/fabianan)

---

