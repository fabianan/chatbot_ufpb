from langchain.memory import ConversationBufferMemory

# Função para inicializar a memória da conversa
def inicializar_memoria():
    # Memória de conversa que mantém o histórico de interações com o usuário
    memory = ConversationBufferMemory(return_messages=True)
    return memory
