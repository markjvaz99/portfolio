from llama_index.core import VectorStoreIndex
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.ollama import OllamaEmbedding  # ✅ ADD

from qdrant_client import QdrantClient
from app.config import *


def get_query_engine():
    client = QdrantClient(url=QDRANT_URL)

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME
    )

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    llm = Ollama(
        model=LLM_MODEL,
        base_url=OLLAMA_BASE_URL,
        additional_kwargs={
            "num_ctx": 2048,  
            "num_predict": 256
        }
    )

    # ✅ ADD THIS (CRITICAL)
    embed_model = OllamaEmbedding(
        model_name=EMBED_MODEL,
        base_url=OLLAMA_BASE_URL
    )

    # ✅ PASS embed_model HERE
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        storage_context=storage_context,
        embed_model=embed_model
    )

    # ✅ ALSO PASS HERE (important in newer versions)
    return index.as_query_engine(
        llm=llm,
        embed_model=embed_model
    )


def query_rag(query: str):
    engine = get_query_engine()
    response = engine.query(query)
    return str(response)
