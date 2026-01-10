import faiss
import numpy as np

from app.utils.chunking import chunk_text
from app.llm.embedding import embed_text  # whatever embedding function you already use

# -------------------------
# FAISS SETUP
# -------------------------

EMBEDDING_DIM = 1536  # match your embedding model
index = faiss.IndexFlatL2(EMBEDDING_DIM)

# Parallel metadata store
# FAISS index position i  <->  chunk_store[i]
chunk_store = []


# -------------------------
# ADD DOCUMENT (CHUNK-BASED)
# -------------------------

def add_document(document_id: int, content: str):
    """
    Split document into chunks and index each chunk separately.
    """

    chunks = chunk_text(content)

    for chunk in chunks:
        embedding = embed_text(chunk)
        embedding = np.array([embedding]).astype("float32")

        index.add(embedding)

        chunk_store.append({
            "document_id": document_id,
            "text": chunk
        })

    print(f"Indexed {len(chunks)} chunks for document {document_id}")


# -------------------------
# SEMANTIC SEARCH (CHUNK-BASED)
# -------------------------

def search_documents(query: str, top_k: int = 5):
    """
    Search relevant chunks for a query.
    Returns list of chunks with document_id + text.
    """

    if index.ntotal == 0:
        return []

    query_embedding = embed_text(query)
    query_embedding = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(chunk_store):
            results.append(chunk_store[idx])

    return results
