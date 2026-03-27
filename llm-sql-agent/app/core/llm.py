from langchain_community.llms import Ollama
from app.core.config import OLLAMA_MODEL, OLLAMA_URL

def get_llm():
    return Ollama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_URL
    )