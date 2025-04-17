# Assistente Institucional da UFPB
Aplicativo que utiliza RAG (Retrieval-Augmented Generation) com Streamlit e LangChain para auxiliar com dúvidas institucionais, orientações de sistemas e direcionamentos.


# Chatbot Institucional UFPB com RAG

Este projeto implementa um chatbot institucional com **RAG (Retrieval-Augmented Generation)** para auxiliar docentes, técnicos, estudantes e gestores da UFPB na consulta a documentos normativos, editais, resoluções e bases de conhecimento. A aplicação utiliza modelos de linguagem generativa integrados a um mecanismo de busca semântica sobre documentos vetorizados.

## Como Executar a Aplicação Localmente

1. **Clone o repositório:**

git clone https://github.com/seu-usuario/chatbot-ufpb.git
cd chatbot-ufpb

2. **Instale as dependências:**

pip install -r requirements.txt

3. **Configure suas variáveis de ambiente:**
Crie um arquivo .env na raiz do projeto com sua chave da API, por exemplo:

OPENAI_API_KEY=your_api_key_here
HF_API_TOKEN=your_api_key_here
GEMINI_API_KEY=your_api_key_here

4. **Execute o app:**

streamlit run .\app\main.py

* Dica: ofereça contexto às questões, como "Sou aluno de pós-graduação em que turmas devo me matricular para o período 2025.1?"

# 🧠 Principais Tecnologias

    Python + Streamlit

    Retrieval-Augmented Generation (RAG)

    Modelos LLM (Gemini, LLaMA, etc.)

    Armazenamento vetorial com FAISS

    PDF/Text parsing + Embedding

    Integração com base BookStack e JSON de unidades