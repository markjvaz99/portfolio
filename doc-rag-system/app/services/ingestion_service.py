import os
from llama_index.core import VectorStoreIndex, Document
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import StorageContext

from qdrant_client import QdrantClient

from app.config import *
from app.utils.hashing import file_hash
from app.services.file_tracker import init_db, is_processed, mark_processed


def ingest():
    init_db()

    client = QdrantClient(url=QDRANT_URL)

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME
    )

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    embed_model = OllamaEmbedding(
        model_name=EMBED_MODEL,
        base_url=OLLAMA_BASE_URL
    )

    documents = []

    for filename in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, filename)

        if not os.path.isfile(path):
            continue

        f_hash = file_hash(path)

        if is_processed(filename, f_hash):
            continue

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        documents.append(
            Document(
                text=text,
                metadata={"filename": filename}
            )
        )

        mark_processed(filename, f_hash)

    if not documents:
        print("No new documents to ingest")
        return

    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model
    )

    print(f"Ingested {len(documents)} documents")
