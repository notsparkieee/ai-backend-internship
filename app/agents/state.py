from typing import TypedDict, List


class AgentState(TypedDict):
    question: str
    intent: str
    documents: List[str]
    answer: str
