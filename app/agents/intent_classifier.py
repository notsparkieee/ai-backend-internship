from app.llm.azure_client import chat_completion


def classify_intent(question: str) -> str:
    """
    Classifies user intent into:
    - document_query
    - general_query
    """

    prompt = f"""
You are an intent classifier.

Classify the user's question into ONE of the following labels:
- document_query
- general_query

Only return the label. No explanation.

Question:
{question}
"""

    response = chat_completion([prompt])

    return response.strip().lower()
