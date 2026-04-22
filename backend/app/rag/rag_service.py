from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import os

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

    db = Chroma.from_documents(docs, embeddings, persist_directory="app/rag/chroma_db")

    return db


# 🔹 crear QA
def crear_qa():
    db = Chroma(persist_directory="app/rag/chroma_db",
                embedding_function=SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2"))

    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(),  # o luego Ollama
        retriever=db.as_retriever()
    )

    return qa