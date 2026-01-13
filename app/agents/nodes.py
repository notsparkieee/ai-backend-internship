from app.agents.state import AgentState
from app.vector_store import has_documents_for_owner
import re

def intent_node(state: AgentState) -> AgentState:
    """Determine if we should try retrieving from user's documents.
    
    Strategy: Check for document-related keywords to decide intent.
    """
    question = state["question"].lower()
    owner_id = state["owner_id"]
    
    # Check if user has any documents
    has_docs = has_documents_for_owner(owner_id)
    
    if not has_docs:
        print(f"User {owner_id} has no documents - general query")
        state["intent"] = "general_query"
        return state
    
    # Document-related keywords that indicate user wants info from their docs
    doc_keywords = [
        r'\b(this|the|my)\s+(doc|document|file|pdf|text)\b',
        r'\bsummarize\b',
        r'\bwhat.*in\s+(this|it|here|the doc)\b',
        r'\btell me about\s+(this|it)\b',
        r'\bexplain\s+(this|it)\b',
        r'\buploaded\b',
        r'\babove\b',
        r'\bprovided\b',
        r'\bcontent\b.*\b(document|file)\b',
        r'\blist.*\b(from|in)\b.*\b(doc|document)\b',
        r'\bfind.*\b(in|from)\b.*\b(doc|document)\b',
        r'\bshow.*\b(from|in)\b.*\b(doc|document)\b',
    ]
    
    # Check for document keywords
    has_doc_keywords = any(re.search(pattern, question) for pattern in doc_keywords)
    
    if has_doc_keywords:
        print(f"Document keywords detected - will retrieve")
        state["intent"] = "document_query"
    else:
        # No explicit doc keywords, but user has docs
        # Try retrieval anyway, let answer_node decide based on scores
        print(f"No doc keywords, but user has docs - will try retrieval")
        state["intent"] = "document_query"
    
    return state
