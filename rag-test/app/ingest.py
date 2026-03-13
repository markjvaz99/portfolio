# 1. Correct (from langchain-community)
from langchain_community.document_loaders import TextLoader 

# 2. Correct (from langchain-text-splitters)
from langchain_text_splitters import RecursiveCharacterTextSplitter 

# 3. Recommended Update (from dedicated langchain-chroma package)
# Instead of: from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import Chroma

# 4. Correct (from dedicated langchain-huggingface package)
from langchain_huggingface.embeddings import HuggingFaceEmbeddings


def ingest_docs():

    loader = TextLoader("data/sample.txt")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    db = Chroma.from_documents(chunks, embeddings, persist_directory="db")

    db.persist()

    print("Documents indexed")

print("Ingesting Docs")
ingest_docs()
print("Ingesting Completed")