from langgraph.graph import StateGraph, END
from app.graph.state import GraphState

from app.graph.nodes.planner import planner_node
from app.graph.nodes.sql_generator import sql_generator_node
from app.graph.nodes.validator import validator_node
from app.graph.nodes.executor import executor_node
from app.graph.nodes.formatter import formatter_node

def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("planner", planner_node)
    graph.add_node("generate_sql", sql_generator_node)
    graph.add_node("validate", validator_node)
    graph.add_node("execute", executor_node)
    graph.add_node("format", formatter_node)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "generate_sql")
    graph.add_edge("generate_sql", "validate")

    graph.add_conditional_edges(
        "validate",
        lambda state: "execute" if state["valid"] else "generate_sql"
    )

    graph.add_edge("execute", "format")
    graph.add_edge("format", END)

    return graph.compile()