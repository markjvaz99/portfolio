from app.core.db import get_connection

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Create tables
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        user_id INT,
        amount FLOAT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """)

    # Check if data exists
    cur.execute("SELECT COUNT(*) FROM users;")
    user_count = cur.fetchone()[0]

    if user_count == 0:
        # Insert sample users
        cur.execute("""
        INSERT INTO users (name) VALUES
        ('Alice'),
        ('Bob'),
        ('Charlie');
        """)

        # Insert sample orders
        cur.execute("""
        INSERT INTO orders (user_id, amount) VALUES
        (1, 100.5),
        (1, 200.0),
        (2, 50.75),
        (3, 300.25);
        """)

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "Database initialized"}