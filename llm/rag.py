# llm/rag.py
import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.ollama import OllamaEmbeddings


# CONFIG – Use absolute paths
PROJECT_DIR = r"C:\Users\aldan\Documents\Aldana UNI\Senior work\simulate-to-educate"
DOCS_FOLDER = os.path.join(PROJECT_DIR, "KnowledgeBase", "RAG_Docs")
VECTOR_DB_DIR = os.path.join(PROJECT_DIR, "KnowledgeBase", "vector_db")
COLLECTION_NAME = "phishing_kb"


# Step 1: Load documents
docs = []
for file_name in os.listdir(DOCS_FOLDER):
    if file_name.endswith(".txt"):
        file_path = os.path.join(DOCS_FOLDER, file_name)
        loader = TextLoader(file_path)
        docs.extend(loader.load())

print(f"[INFO] Loaded {len(docs)} documents from {DOCS_FOLDER}")


# Step 2: Split documents into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs_split = splitter.split_documents(docs)

print(f"[INFO] Split documents into {len(docs_split)} chunks")


# Step 3: Create embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text") 
vector_db = Chroma.from_documents(
    docs_split,
    embeddings,
    collection_name=COLLECTION_NAME,
    persist_directory=VECTOR_DB_DIR
)


# Step 4: Persist the vector DB
vector_db.persist()
print(f"[INFO] RAG knowledge base created and saved at {VECTOR_DB_DIR}")


# Step 5: Quick verification 
results = vector_db.similarity_search("suspicious link in email", k=2)
print("\n[INFO] Sample search results:")
for i, r in enumerate(results, 1):
    print(f"--- Result {i} ---")
    print(r.page_content[:200], "...\n")

def retrieve_docs(query, k=3):
    return vector_db.similarity_search(query, k=k)


# retrival function
def retrieve_context(query, k=3):
    results = vector_db.similarity_search(query, k=k)
    return "\n".join([doc.page_content for doc in results])

