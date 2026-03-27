def formatter_node(state):
    if state.get("error"):
        state["final_answer"] = {
            "type": "error",
            "message": state["error"]
        }
        return state

    # Just pass structured result
    state["final_answer"] = state["result"]
    return state