from fastapi import FastAPI
from .rag_pipeline import query_rag
from .llm_pipeline import ask_llm_zero_shot, ask_llm_one_shot, ask_llm_few_shot, ask_llm_chain_of_thought

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Local RAG running not updated"}

@app.post("/ask_llm_zero_shot")
def ask_llm_phi(question: str):

    answer = ask_llm_zero_shot(question)

    return {
        "question": question,
        "answer": answer
    }

@app.post("/ask_llm_one_shot")
def ask_llm_phi(question: str):

    answer = ask_llm_one_shot(question)

    return {
        "question": question,
        "answer": answer
    }

@app.post("/ask_llm_few_shot")
def ask_llm_phi(question: str):

    answer = ask_llm_few_shot(question)

    return {
        "question": question,
        "answer": answer
    }

@app.post("/ask_llm_chain_of_thought")
def ask_llm_phi(question: str):

    answer = ask_llm_chain_of_thought(question)

    return {
        "question": question,
        "answer": answer
    }

@app.post("/query")
def ask(question: str):

    answer = query_rag(question)

    return {
        "question": question,
        "answer": answer
    }
