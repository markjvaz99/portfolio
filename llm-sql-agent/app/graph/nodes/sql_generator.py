from app.core.llm import get_llm
from app.services.schema_loader import get_schema

llm = get_llm()

def clean_sql(sql: str) -> str:
    # Remove markdown code blocks
    sql = sql.strip()

    if sql.startswith("```"):
        sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql

def sql_generator_node(state):
    schema = get_schema()

    prompt = f"""
You are a PostgreSQL expert.

Schema:
{schema}

Convert this to SQL:
{state['user_query']}

Rules:
- Only SELECT queries
- No markdown
- No explanation
- Return ONLY raw SQL
"""

    sql = llm.invoke(prompt)

    cleaned_sql = clean_sql(sql)

    state["sql_query"] = cleaned_sql
    return state