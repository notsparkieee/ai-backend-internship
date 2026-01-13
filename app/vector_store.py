import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

DIMENSION = 384

# FAISS index (cosine similarity using inner product)
index = faiss.IndexFlatIP(DIMENSION)

# Map FAISS index position -> document_id
doc_id_map = []


def embed_text(text: str):
    vector = model.encode([text])
    return np.array(vector).astype("float32")


def add_document(document_id: int, text: str):
    vector = embed_text(text)
    index.add(vector)
    doc_id_map.append(document_id)


def search_documents(query: str, top_k: int = 5):
    query_vector = embed_text(query)
    scores, indices = index.search(query_vector, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(doc_id_map):
            results.append(doc_id_map[idx])

    return results
