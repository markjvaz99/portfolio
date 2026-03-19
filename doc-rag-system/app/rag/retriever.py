from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.retrievers import QueryFusionRetriever


def get_hybrid_retriever(index, llm):

    vector_retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=3
    )

    try:
        nodes = list(index.docstore.docs.values())

        if len(nodes) == 0:
            raise ValueError("No nodes for BM25")

        bm25_retriever = BM25Retriever.from_defaults(
            nodes=nodes,
            similarity_top_k=3
        )

        hybrid_retriever = QueryFusionRetriever(
            [vector_retriever, bm25_retriever],
            similarity_top_k=3,
            num_queries=1,
            mode="reciprocal_rerank",
            llm=llm
        )

        return hybrid_retriever

    except Exception:
        return vector_retriever

