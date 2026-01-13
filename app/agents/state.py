from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    question: str
    owner_id: int
    intent: Optional[str]
    retrieved_chunks: Optional[List[dict]]
    answer: Optional[str]
