import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "port": 5432,
    "database": "mydb",
    "user": "user",
    "password": "pass"
}

OLLAMA_MODEL = "llama3.2:1b"
OLLAMA_URL = "http://ollama:11434"