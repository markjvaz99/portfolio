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

def query_rag(question):

    docs = db.similarity_search(question, k=3)

    context = "\n".join([d.page_content for d in docs])

    print("Context >>>", context)

    prompt = f"""
                You are a helpful assistant. Answer the question using ONLY the provided context. The answer should be limited to 3-5 words

                Context:
                {context}

                Question:
                {question}

                Answer:
                """

    response = client.chat(
        model="phi3:mini",
        messages=[{"role": "user", "content": prompt}],
        # options={
        #     "num_predict": 5,
        #     "temperature": 0.5
        # }
    )


    return response["message"]["content"]

def ask_llm(question, temperature=0.7, max_tokens=200):

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
