import re

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 200):
    """Split text into chunks with sentence-aware boundaries.
    
    Args:
        text: Text to chunk
        chunk_size: Target size per chunk (chars)
        overlap: Overlap between chunks (chars)
    """
    text = text.strip()
    
    if not text:
        return []
    
    # For short text, return as single chunk
    if len(text) <= chunk_size:
        return [text]
    
    # Split into sentences
    sentence_endings = re.compile(r'[.!?]\s+')
    sentences = sentence_endings.split(text)
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # If adding this sentence exceeds chunk_size, save current chunk
        if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            # Keep last overlap chars for context
            current_chunk = current_chunk[-overlap:] + " " + sentence if len(current_chunk) > overlap else sentence
        else:
            current_chunk += (" " if current_chunk else "") + sentence
    
    # Add final chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks if chunks else [text]
