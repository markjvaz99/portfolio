from app.core.db import get_connection

def executor_node(state):
    if not state.get("valid"):
        return state

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(state["sql_query"])

        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()

        # 🔥 JSON-ready structure
        state["result"] = {
            "type": "table",
            "columns": columns,
            "rows": rows,
            "row_count": len(rows)
        }

    except Exception as e:
        state["error"] = str(e)

    return state