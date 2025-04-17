import os
from langchain import hub
from langchain_core.runnables import RunnablePassthrough, RunnableMap
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import HuggingFaceEndpoint
from langchain.llms import HuggingFacePipeline
from transformers import pipeline

from utils import formatar_documentos
from langchain_openai import ChatOpenAI



# Função para formatar as unidades negociais
def formatar_unidades(unidades):
    return "\n".join([
        f"- {sigla}: {dados['nome']} | Email: {dados['email']} | Tel: {dados.get('telefone', 'N/D')} | Site: {dados.get('site', 'N/D')}"
        for sigla, dados in unidades.items()
    ])

# Função para identificar a unidade responsável pela pergunta
def identificar_unidade_responsavel(pergunta, unidades):
    pergunta_lower = pergunta.lower()
    melhor_unidade = None
    maior_pontuacao = 0

    for sigla, dados in unidades.items():
        atribuicoes = [a.strip().lower() for a in dados.get("atribuicao", "").split(",")]
        pontuacao = sum(1 for palavra in atribuicoes if palavra in pergunta_lower)
        if pontuacao > maior_pontuacao:
            maior_pontuacao = pontuacao
            melhor_unidade = dados

    if melhor_unidade and maior_pontuacao > 0:
        return (f"Com base na sua pergunta, a unidade responsável parece ser **{melhor_unidade['nome']}**.\n"
                f"Email: {melhor_unidade['email']}\n"
                f"Telefone: {melhor_unidade['telefone']}\n"
                f"Site: {melhor_unidade['site']}\n")
    return ""

# Função para montar o pipeline RAG
def montar_rag(vector_db, unidades_negociais, n_documentos=20):
    #from langchain_google_genai import ChatGoogleGenerativeAI
    from dotenv import load_dotenv

    # Carrega variáveis de ambiente 
    load_dotenv()
    
    #GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Inicializa o LLM com o modelo do Google Generative AI
    #llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GEMINI_API_KEY)
    
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4o-mini")

   # API_TOKEN = os.getenv("HF_API_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN")
   # MODEL_NAME ="meta-llama/Meta-Llama-3-8B-Instruct"

    #llm = HuggingFaceEndpoint(
    #    endpoint_url=f"https://api-inference.huggingface.co/models/{MODEL_NAME}",
    #    huggingfacehub_api_token=API_TOKEN,
    #    task="text-generation",
    #    max_new_tokens=500,
    #)
    

    # Memória de conversa
    memory = ConversationBufferMemory(return_messages=True)

    unidades_texto = formatar_unidades(unidades_negociais)

    # Função para obter o histórico de mensagens
    def get_chat_history(inputs):
        return memory.chat_memory.messages


    def identificar_e_incluir(inputs):
        pergunta = inputs["question"]
        contexto = inputs["context"]

        # Diagnóstico de retorno do banco vetorial
        print(f"\nPergunta: {pergunta}\nContexto recuperado:\n{contexto[:1500]}\n{'-'*50}\n")

        complemento = identificar_unidade_responsavel(pergunta, unidades_negociais)
        inputs["context"] += "\n\n" + complemento
        return inputs


    # Template do prompt para interação
    prompt = PromptTemplate(
        input_variables=["context", "question", "chat_history", "unidades_texto"],
        template="""
        Você é um assistente institucional da UFPB. Sempre utilize os documentos abaixo para responder à pergunta do usuário.
        Dê prioridade máxima ao conteúdo legal e normativo dos documentos. Caso a pergunta mencione algum artigo, capítulo ou resolução específica (ex: "Art. 75 da Resolução 54/2024"), 
        **busque exatamente esse trecho nos documentos** antes de qualquer outra ação.

        Só oriente o usuário a procurar outro setor **se a informação não estiver realmente nos documentos**.

        Unidades Negociais:
        {unidades_texto}

        Histórico da conversa:
        {chat_history}

        Contexto:
        {context}

        Pergunta:
        {question}
        """
    )

    # Cria o pipeline de consulta com o banco vetorial e o modelo
    rag = (
        RunnableMap({
            "question": RunnablePassthrough(),
            "context": vector_db.as_retriever(search_type="mmr", search_kwargs={"k": n_documentos, "lambda_mult": 0.8}) | formatar_documentos,
            "chat_history": get_chat_history
        })
        | identificar_e_incluir
        | prompt.partial(unidades_texto=unidades_texto)
        | llm
        | StrOutputParser()
    )

    return rag, memory



