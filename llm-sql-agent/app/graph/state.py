from typing import TypedDict, Optional

class GraphState(TypedDict):
    user_query: str
    sql_query: Optional[str]
    result: Optional[str]
    final_answer: Optional[str]
    error: Optional[str]
    valid: Optional[bool]