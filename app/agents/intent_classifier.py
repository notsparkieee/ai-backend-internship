from app.llm.azure_client import chat_completion


def classify_intent(question: str) -> str:
    prompt = f"""
Classify the user's question into ONE of the following:
- document_query
- general_query

Return only the label.

Question:
{question}
"""

    response = chat_completion([prompt])
    return response.strip().lower()
