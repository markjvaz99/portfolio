from fastapi import FastAPI
from app.graph.builder import build_graph
from app.services.db_init import init_db

app = FastAPI()
graph = build_graph()

@app.post("/query")
def query(data: dict):
    result = graph.invoke({
        "user_query": data["query"]
    })

    return {
        "sql": result.get("sql_query"),
        "data": result.get("final_answer")
    }


@app.post("/init-db")
def initialize_database():
    return init_db()