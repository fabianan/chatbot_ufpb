import json
import os

# Função para carregar as URLs dos PDFs
def carregar_urls():
    with open(os.path.join("data", "urls.json"), "r", encoding="utf-8") as f:
        return json.load(f)

# Função para carregar as unidades negociais
def carregar_unidades():
    with open(os.path.join("data", "unidades_negociais.json"), "r", encoding="utf-8") as f:
        return json.load(f)

# Função para carregar os dados dos usuários
def carregar_usuarios():
    with open(os.path.join("data", "usuarios.json"), "r", encoding="utf-8") as f:
        return json.load(f)
