def validator_node(state):
    sql = state["sql_query"]

    # Remove accidental markdown again (extra safety)
    sql = sql.replace("```", "").strip()
    state["sql_query"] = sql

    forbidden = ["DELETE", "UPDATE", "INSERT", "DROP"]

    if any(word in sql.upper() for word in forbidden):
        state["valid"] = False
        state["error"] = "Unsafe query detected"
    else:
        state["valid"] = True

    return state