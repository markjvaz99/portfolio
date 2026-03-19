import sqlite3
from app.config import DB_PATH

conn = sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn.execute("""
        CREATE TABLE IF NOT EXISTS files (
            filename TEXT PRIMARY KEY,
            hash TEXT
        )
    """)

def is_processed(filename, hash_val):
    cur = conn.execute(
        "SELECT hash FROM files WHERE filename=?",
        (filename,)
    )
    row = cur.fetchone()
    return row and row[0] == hash_val

def mark_processed(filename, hash_val):
    conn.execute(
        "REPLACE INTO files (filename, hash) VALUES (?, ?)",
        (filename, hash_val)
    )
    conn.commit()
