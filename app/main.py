import os
import json
import streamlit as st
from dotenv import load_dotenv

from loader import baixar_pdfs, carregar_banco_vetorial, extrair_titulo_pdf
from rag import montar_rag
from memory import inicializar_memoria
from db import carregar_urls, carregar_unidades
from utils import formatar_documentos




# Configuração da página
st.set_page_config(page_title="Assistente UFPB", layout="wide")
st.title("Assistente Institucional da UFPB")

# Carrega variáveis de ambiente
load_dotenv()

# Carrega dados do diretório /data
URLS_PDF = carregar_urls()
UNIDADES_NEGOCIAIS = carregar_unidades()

# Baixa PDFs e monta banco vetorial
baixar_pdfs(URLS_PDF)

REINDEXAR_VETORES = False  # True quando quiser forçar reindexação

vector_db = carregar_banco_vetorial(reindexar=REINDEXAR_VETORES)


# Inicializa RAG e memória na sessão
if "memory" not in st.session_state:
    st.session_state.rag, st.session_state.memory = montar_rag(vector_db, UNIDADES_NEGOCIAIS)
memory = st.session_state.memory
rag = st.session_state.rag

if "historico" not in st.session_state:
    st.session_state.historico = []

# Exibe documentos na barra lateral
with st.sidebar:
    st.header("📄 Documentos carregados")
    for nome_arquivo in os.listdir("pdfs"):
        if nome_arquivo.endswith(".pdf"):
            caminho = os.path.join("pdfs", nome_arquivo)
            titulo = extrair_titulo_pdf(caminho)
            st.markdown(f"- {titulo}")
    if st.button("🔁 Reindexar documentos"):
        with st.spinner("Reindexando base vetorial..."):
            vector_db = carregar_banco_vetorial(reindexar=True)
            st.session_state.rag, st.session_state.memory = montar_rag(vector_db, UNIDADES_NEGOCIAIS)
            rag = st.session_state.rag
            memory = st.session_state.memory
            st.success("Base vetorial atualizada!")
    if st.button("🚪 Sair"):
        st.stop()

# Mensagem inicial
with st.chat_message("assistant"):
    st.markdown("Olá! Sou o assistente institucional da UFPB. Como posso ajudar você hoje?")

# Histórico da conversa
for pergunta, resposta in st.session_state.historico:
    with st.chat_message("user"):
        st.markdown(pergunta)
    with st.chat_message("assistant"):
        st.markdown(resposta)

# Interação com o usuário
if pergunta := st.chat_input("Digite sua pergunta..."):
    with st.chat_message("user"):
        st.markdown(pergunta)

    resposta = rag.invoke(pergunta)
    with st.chat_message("assistant"):
        st.markdown(resposta)

    # Atualiza histórico
    st.session_state.historico.append((pergunta, resposta))
    memory.chat_memory.add_user_message(pergunta)
    memory.chat_memory.add_ai_message(resposta)
