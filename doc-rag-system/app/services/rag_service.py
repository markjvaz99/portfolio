from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from qdrant_client import QdrantClient

from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.postprocessor.sbert_rerank import SentenceTransformerRerank

from app.rag.retriever import get_hybrid_retriever
from app.rag.threshold_reranker import ScoreThresholdPostprocessor
from app.rag.synthesizer import get_synthesizer
from app.config import *


def run_rag_pipeline(query: str, logger=None, request_id=None):

    # ---------------------------
    # Qdrant + Index
    # ---------------------------
    client = QdrantClient(url=QDRANT_URL)

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME
    )

    embed_model = OllamaEmbedding(
        model_name=EMBED_MODEL,
        base_url=OLLAMA_BASE_URL,
        request_timeout=120.0
    )

    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=embed_model
    )


    # ---------------------------
    # Reranker
    # ---------------------------
    reranker = SentenceTransformerRerank(
        model="cross-encoder/ms-marco-MiniLM-L-6-v2",
        top_n=3
    )

    # ---------------------------
    # LLM
    # ---------------------------
    llm = Ollama(
        model=LLM_MODEL,
        base_url=OLLAMA_BASE_URL,
        request_timeout=300.0,
        temperature=0,
        additional_kwargs={
            "num_ctx": 1024,
            "num_predict": 128
        }
    )
    # ---------------------------
    # Hybrid Retriever
    # ---------------------------
    retriever = get_hybrid_retriever(index, llm)

    # ---------------------------
    # Synthesizer
    # ---------------------------
    synthesizer = get_synthesizer(llm)

    # ---------------------------
    # Query Engine
    # ---------------------------
    score_filter = ScoreThresholdPostprocessor(threshold=0.0)

    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=synthesizer,
        node_postprocessors=[reranker, score_filter]
    )
    # query_engine = RetrieverQueryEngine(
    #     retriever=retriever,
    #     response_synthesizer=synthesizer,
    #     node_postprocessors=[reranker]
    # )

    response = query_engine.query(query)

    # ---------------------------
    # Logging sources
    # ---------------------------
    sources = []
    if hasattr(response, "source_nodes"):
        for node in response.source_nodes:
            if logger:
                logger.info(
                    f"[{request_id}] FINAL | Score: {node.score:.4f} | {node.text}"
                )
            sources.append({
                "text": node.text,
                "score": node.score
            })

    return str(response), sources
