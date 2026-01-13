import faiss
import numpy as np
import pickle
import os
from app.llm.embedding import embed_text, DIM
from app.utils.chunking import chunk_text

INDEX_FILE = 'vector_index.faiss'
METADATA_FILE = 'chunk_metadata.pkl'

def save_index():
    faiss.write_index(index, INDEX_FILE)
    with open(METADATA_FILE, 'wb') as f:
        pickle.dump(chunk_metadata, f)

def load_index():
    global index, chunk_metadata
    if os.path.exists(INDEX_FILE):
        print(f"Loading index from {INDEX_FILE}")
        index = faiss.read_index(INDEX_FILE)
        print(f"Loaded index with {index.ntotal} vectors")
    else:
        print("No saved index file found")
    if os.path.exists(METADATA_FILE):
        print(f"Loading metadata from {METADATA_FILE}")
        with open(METADATA_FILE, 'rb') as f:
            chunk_metadata = pickle.load(f)
        print(f"Loaded {len(chunk_metadata)} metadata entries")
    else:
        print("No saved metadata file found")

# Load on startup
index = faiss.IndexFlatL2(DIM)
chunk_metadata = []
load_index()

# FAISS index position == metadata position
# each item: { "document_id": int, "owner_id": int, "text": str }

def index_document_chunks(document_id: int, content: str, owner_id: int):
    print(f"Indexing document {document_id} for owner {owner_id}, content length: {len(content)}")
    chunks = chunk_text(content)
    print(f"Created {len(chunks)} chunks")

    for i, chunk in enumerate(chunks):
        print(f"Embedding chunk {i}: {chunk[:50]}...")
        vector = np.array(embed_text(chunk), dtype="float32").reshape(1, -1)
        index.add(vector)

        chunk_metadata.append({
            "document_id": document_id,
            "owner_id": owner_id,
            "text": chunk
        })
    
    print(f"Total indexed: {index.ntotal}")
    # Save after indexing
    save_index()
    print("Saved index to disk")

def has_documents_for_owner(owner_id: int) -> bool:
    """Check if there are any indexed documents for this owner."""
    return any(meta["owner_id"] == owner_id for meta in chunk_metadata)

def search_similar_chunks(query: str, owner_id: int, top_k: int = 5):
    """Search for similar chunks from owner's documents.
    
    Args:
        query: Search query
        owner_id: Filter by document owner
        top_k: Number of chunks to return
    """
    if index.ntotal == 0:
        return []

    # Get all chunks for this owner
    owner_chunks = [(i, meta) for i, meta in enumerate(chunk_metadata) if meta["owner_id"] == owner_id]
    
    if not owner_chunks:
        return []
    
    print(f"Searching {len(owner_chunks)} chunks for owner {owner_id}")
    
    query_vector = np.array(embed_text(query), dtype="float32").reshape(1, -1)
    
    # Search broadly to find owner's chunks
    search_k = min(index.ntotal, max(top_k * 20, 100))
    distances, indices = index.search(query_vector, search_k)

    # Filter by owner and take best matches
    results = []
    for idx, dist in zip(indices[0], distances[0]):
        if idx < len(chunk_metadata) and chunk_metadata[idx]["owner_id"] == owner_id:
            results.append({
                **chunk_metadata[idx],
                "score": float(dist)
            })
            if len(results) >= top_k:
                break
    
    if results:
        print(f"Found {len(results)} chunks, best score: {results[0]['score']:.3f}")
    
    return results
