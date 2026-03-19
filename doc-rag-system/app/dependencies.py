from app.models.ollama_provider import OllamaProvider

def get_llm():
    return OllamaProvider()