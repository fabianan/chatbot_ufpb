def formatar_documentos(docs):
    return "\n\n".join([
        f"Documento: {d.metadata.get('nome', 'Desconhecido')}\n{d.page_content.strip()}"
        for d in docs
    ])
