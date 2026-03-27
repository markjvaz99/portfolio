def get_schema():
    return """
Table: users
- id (int)
- name (text)
- created_at (timestamp)

Table: orders
- id (int)
- user_id (int)
- amount (float)
"""