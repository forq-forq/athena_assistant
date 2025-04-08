import os
from uuid import uuid4
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_pinecone import Pinecone as PineconeStore

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

def get_vectorstore():
    embeddings = OpenAIEmbeddings()
    return PineconeStore(index=index, embedding=embeddings, text_key="text")

def embed_documents(documents: list[Document]) -> None:
    vectorstore = get_vectorstore()

    existing_docs = vectorstore.similarity_search("", k=1000)
    existing_sources = {doc.metadata.get("source") for doc in existing_docs}

    texts = []
    metadatas = []
    ids = []

    for doc in documents:
        source = doc.metadata.get("source")
        if source in existing_sources:
            continue

        for i in range(0, len(doc.page_content), 1000):
            chunk = doc.page_content[i:i+1000]
            uid = str(uuid4())
            texts.append(chunk)
            metadatas.append({
                "id": uid,
                "source": source
            })
            ids.append(uid)

    if texts:
        vectorstore.add_texts(texts=texts, metadatas=metadatas, ids=ids)

def get_all_documents():
    vectorstore = get_vectorstore()
    return vectorstore.similarity_search(query="", k=1000)

def delete_document_by_source(source_name: str) -> bool:
    docs = get_all_documents()
    ids_to_delete = [
        doc.metadata.get("id") for doc in docs
        if doc.metadata.get("source") == source_name and doc.metadata.get("id")
    ]
    if ids_to_delete:
        index.delete(ids=ids_to_delete)
        return True
    return False
