from bookstack_loader import carregar_base_bookstack

bookstack_docs = carregar_base_bookstack()
print(f"🔢 Total de documentos carregados: {len(bookstack_docs)}\n")

for i, doc in enumerate(bookstack_docs[:3], 1):  # Mostra só os 3 primeiros
    print(f"\n📘 Documento {i}")
    print(f"Fonte: {doc.metadata['source']}")
    print(f"Conteúdo (resumo):\n{doc.page_content[:500]}...\n")

