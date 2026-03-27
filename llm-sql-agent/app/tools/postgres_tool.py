from langchain.tools import tool
from app.core.db import get_connection

@tool
def query_postgres(sql: str) -> str:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    return str(cur.fetchall())