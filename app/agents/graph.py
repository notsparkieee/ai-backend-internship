from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.intent_classifier import classify_intent
from app.agents.retrieval_node import retrieval_node
from app.agents.answer_node import answer_node


def intent_node(state):
    state["intent"] = classify_intent(state["question"])
    return state


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
        "general_query": "answer",
    }
)

graph.add_edge("retrieve", "answer")
graph.add_edge("answer", END)

qa_agent = graph.compile()
