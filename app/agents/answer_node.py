from app.llm.azure_client import chat_completion
import re

def answer_node(state):
    question = state["question"]

    # Use chunks if any were retrieved
    if state.get("retrieved_chunks") and len(state["retrieved_chunks"]) > 0:
        context = "\n\n".join(chunk["text"] for chunk in state["retrieved_chunks"])
        best_score = state["retrieved_chunks"][0].get("score", 999)
        
        # Document-related keywords (user explicitly asking about docs)
        doc_keywords = [
            r'\b(this|the|my)\s+(doc|document|file|pdf|text)\b',
            r'\bsummarize\b',
            r'\bwhat.*in\s+(this|it|here|the doc)\b',
            r'\btell me about\s+(this|it)\b',
            r'\bexplain\s+(this|it)\b',
            r'\buploaded\b',
            r'\babove\b',
            r'\bprovided\b',
        ]
        
        question_lower = question.lower()
        has_doc_keywords = any(re.search(pattern, question_lower) for pattern in doc_keywords)
        
        # HYBRID DECISION:
        # 1. If explicit doc keywords → Always use context
        # 2. If no keywords but good similarity (< 0.8) → Use context  
        # 3. If no keywords and poor similarity (> 0.8) → General answer
        
        should_use_context = has_doc_keywords or best_score < 0.8
        
        if should_use_context:
            # Use document context
            prompt = f"""You are a helpful AI assistant. The user has uploaded documents to your system and you have direct access to their content below.

IMPORTANT INSTRUCTIONS:
- The content below IS the user's document - you have full access to it
- NEVER say you cannot access documents or files when context is provided
- Answer the question directly based on the information given below
- If the answer is in the context, provide it confidently
- If you're not sure, say "Based on the provided document" and give your best answer

DOCUMENT CONTENT:
{context}

USER QUESTION: {question}

Answer the question based on the document content above:"""
            answer = chat_completion([prompt])
            # Extract first sentence
            first_sentence = answer.split('.')[0] + '.' if '.' in answer else answer
            formatted_answer = f"This is from document: {first_sentence}\n\n{answer}"
        else:
            # Poor match and no doc keywords - use general answer
            print(f"Poor match (score={best_score:.3f}) with no doc keywords - general answer")
            answer = chat_completion([question])
            formatted_answer = f"This is not from documents.\n\n{answer}"
    else:
        answer = chat_completion([question])
        formatted_answer = f"This is not from documents.\n\n{answer}"

    state["answer"] = formatted_answer
    return state
