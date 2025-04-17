import os
import urllib.request

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Função para baixar os PDFs das URLs fornecidas
def baixar_pdfs(urls):
    os.makedirs("pdfs", exist_ok=True)
    for url in urls:
        try:
            if "idArquivo=" in url:
                nome_arquivo = url.split("idArquivo=")[1].split("&")[0] + ".pdf"
            else:
                nome_arquivo = os.path.basename(url.split("?")[0]) or f"arquivo_{abs(hash(url))}.pdf"
        except Exception:
            nome_arquivo = f"arquivo_{abs(hash(url))}.pdf"

        caminho = os.path.join("pdfs", nome_arquivo)
        if not os.path.exists(caminho):
            urllib.request.urlretrieve(url, caminho)


# Função para carregar ou criar o banco vetorial com persistência
def carregar_banco_vetorial(pasta_persistencia="vector_db", reindexar=False):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    # Se a base já existe e reindexar=False, só carrega
    if not reindexar and os.path.exists(pasta_persistencia) and os.listdir(pasta_persistencia):
       # return Chroma(persist_directory=pasta_persistencia, embedding_function=embeddings)
       return FAISS.load_local(
            folder_path=pasta_persistencia,
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        )

    # Se reindexar=True ou a base ainda não existe, processa tudo de novo
    documentos = []
    for nome_arquivo in os.listdir("pdfs"):
        if nome_arquivo.endswith(".pdf"):
            caminho = os.path.join("pdfs", nome_arquivo)
            dados = PyPDFLoader(caminho).load()
            documentos.extend(dados)

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
    textos = splitter.split_documents(documentos)

    from bookstack_loader import carregar_base_bookstack

    bookstack_docs = carregar_base_bookstack()
    textos.extend(splitter.split_documents(bookstack_docs))

    vector_db = FAISS.from_documents(textos, embeddings) #Chroma.from_documents(textos, embedding=embeddings, persist_directory=pasta_persistencia)
    
    vector_db.save_local(pasta_persistencia)

    return vector_db



# Função para extrair o título de um PDF
from PyPDF2 import PdfReader

def extrair_titulo_pdf(caminho_pdf):
    try:
        reader = PdfReader(caminho_pdf)
        primeira_pagina = reader.pages[0]
        texto = primeira_pagina.extract_text()
        if texto:
            for linha in texto.split("\n"):
                if "RESOLUÇÃO" in linha.upper() or "EDITAL" in linha.upper():
                    return linha.strip()
        return os.path.basename(caminho_pdf)
    except Exception as e:
        return f"Erro ao ler {caminho_pdf}: {e}"
