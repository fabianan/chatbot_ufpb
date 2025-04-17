import os
import requests
from bs4 import BeautifulSoup
from langchain.schema import Document

BOOKSTACK_TOKEN_ID = os.getenv("BOOKSTACK_TOKEN_ID")
BOOKSTACK_TOKEN_SECRET = os.getenv("BOOKSTACK_TOKEN_SECRET")
HEADERS = {
    "Authorization": f"Token {BOOKSTACK_TOKEN_ID}:{BOOKSTACK_TOKEN_SECRET}"
}

def extrair_texto_html(html):
    soup = BeautifulSoup(html, "html.parser")
    texto = soup.get_text(separator="\n", strip=True)
    return texto

def carregar_base_bookstack(caminho_urls=None):
    documentos = []

    if caminho_urls is None:
        # Resolve caminho absoluto para o arquivo que está na pasta /app
        caminho_urls = os.path.join(os.path.dirname(os.path.abspath(__file__)), "base_conhecimento_url.txt")

    if not os.path.exists(caminho_urls):
        print(f"❌ Arquivo não encontrado: {caminho_urls}")
        return documentos

    with open(caminho_urls, "r", encoding="utf-8") as f:
        urls = [linha.strip() for linha in f if linha.strip()]

    for url in urls:
        try:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()

            texto = extrair_texto_html(response.text)

            documentos.append(
                Document(
                    page_content=texto,
                    metadata={"source": url}
                )
            )
            print(f"✅ Documento carregado de: {url}")
        except Exception as e:
            print(f"⚠️ Erro ao carregar {url}: {e}")

    return documentos
