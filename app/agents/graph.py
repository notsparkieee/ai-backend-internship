from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.nodes import intent_node
from app.agents.retrieval_node import retrieval_node
from app.agents.answer_node import answer_node

graph = StateGraph(AgentState)

graph.add_node("intent", intent_node)
graph.add_node("retrieve", retrieval_node)
graph.add_node("answer", answer_node)

graph.set_entry_point("intent")

graph.add_conditional_edges(
    "intent",
    lambda state: state["intent"],
    {
        "document_query": "retrieve",
        "general_query": "answer"
    }
)

graph.add_edge("retrieve", "answer")
graph.add_edge("answer", END)

qa_agent = graph.compile()
