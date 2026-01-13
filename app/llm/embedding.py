from sentence_transformers import SentenceTransformer
import numpy as np

# Load the model once at module level
print("Loading sentence transformer model...")
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    # Warm up the model with a test encoding
    _ = model.encode("test", convert_to_numpy=True)
    print(f"Model loaded successfully! Embedding dimension: {model.get_sentence_embedding_dimension()}")
except Exception as e:
    print(f"ERROR loading model: {e}")
    raise

DIM = 384  # Dimension for all-MiniLM-L6-v2

def embed_text(text: str) -> list[float]:
    """
    Generate semantic embeddings using sentence transformers.
    Returns normalized 384-dimensional vector.
    """
    try:
        embedding = model.encode(text, convert_to_numpy=True, show_progress_bar=False)
        # Normalize the embedding
        embedding = embedding / np.linalg.norm(embedding)
        return embedding.tolist()
    except Exception as e:
        print(f"ERROR in embed_text: {e}")
        raise
