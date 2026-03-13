from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import ollama

client = ollama.Client(host="http://ollama:11434")

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="db",
    embedding_function=embeddings
)

def ask_llm_zero_shot(question, temperature=0.7, max_tokens=200):

    response = client.chat(
        model="phi3:mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ],
        options={
            "temperature": temperature,
            "num_predict": max_tokens
        }
    )

    return response["message"]["content"]


def ask_llm_one_shot(question, temperature=0.7, max_tokens=200):

    prompt = f"""
You are a helpful assistant.

Example 1
Q: What is the capital of France?
A: Answer = Paris.

Now answer the following question.

Q: {question}
A:
"""

    response = client.chat(
        model="phi3:mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        options={
            "temperature": temperature,
            "num_predict": max_tokens
        }
    )

    return response["message"]["content"]



def ask_llm_few_shot(question, temperature=0.7, max_tokens=200):

    prompt = f"""
You are a helpful assistant.

Example 1
Q: What is the capital of France?
A: The capital of France is Paris.

Example 2
Q: What is the capital of Japan?
A: The capital of Japan is Tokyo.

Example 3
Q: What is the capital of Germany?
A: The capital of Germany is Berlin.

Now answer the following question.

Q: {question}
A:
"""

    response = client.chat(
        model="phi3:mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        options={
            "temperature": temperature,
            "num_predict": max_tokens
        }
    )

    return response["message"]["content"]


def ask_llm_chain_of_thought(question, temperature=0.7, max_tokens=200):

    response = client.chat(
        model="phi3:mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Solve the problem step by step before giving the final answer."},
            {"role": "user", "content": question}
        ],
        options={
            "temperature": temperature,
            "num_predict": max_tokens
        }
    )

    return response["message"]["content"]