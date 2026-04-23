from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings


def detectar_tema(pregunta: str):
    pregunta = pregunta.lower()

    if "homolog" in pregunta:
        return "HOMOLOGACIÓN"
    elif "certificado" in pregunta:
        return "CERTIFICADOS"
    elif "cancel" in pregunta:
        return "CANCELACIÓN"
    elif "beca" in pregunta:
        return "BECAS"
    else:
        return None

# 🔹 cargar documentos
def cargar_documentos():
    loader = TextLoader("app/rag/docs/reglamento.txt")
    documents = loader.load()

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    return docs


# 🔹 crear base vectorial
def crear_vectorstore():
    docs = cargar_documentos()

    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    db = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory="app/rag/chroma_db"
    )

    return db


# 🔹 crear QA (SIN OpenAI, modo local simple)
def crear_qa():
    db = Chroma(
        persist_directory="app/rag/chroma_db",
        embedding_function=SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    )

    return db


def buscar_respuesta(pregunta: str):
    db = Chroma(
        persist_directory="app/rag/chroma_db",
        embedding_function=SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    )

    resultados = db.similarity_search(pregunta, k=4)

    if not resultados:
        return "🤔 No encontré información sobre eso."

    tema = detectar_tema(pregunta)

    textos_filtrados = []

    for doc in resultados:
        contenido = doc.page_content

        # 🔥 FILTRAR POR TEMA
        if tema and tema in contenido.upper():
            textos_filtrados.append(contenido)

    # si no encontró por tema, usa lo general
    if not textos_filtrados:
        textos_filtrados = [doc.page_content for doc in resultados[:2]]

    contexto = "\n".join(textos_filtrados)

    respuesta = f"""
🤖 Entendí tu pregunta: "{pregunta}"

📘 Información relevante:

{contexto}

Si necesitas algo más específico, dime 👍
"""

    return respuesta[:800]