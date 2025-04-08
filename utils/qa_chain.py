import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_pinecone import Pinecone as PineconeStore
from langchain_core.documents import Document

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

def answer_question(query: str, custom_documents: list[Document] = None) -> str:
    embeddings = OpenAIEmbeddings()
    vectorstore = PineconeStore(index=index, embedding=embeddings, text_key="text")

    db_docs = vectorstore.similarity_search(query, k=4)

    all_docs = db_docs.copy()
    if custom_documents:
        all_docs.extend(custom_documents)

    unique_docs = []
    seen = set()
    for doc in all_docs:
        identifier = (doc.page_content, doc.metadata.get("source"))
        if identifier not in seen:
            seen.add(identifier)
            unique_docs.append(doc)

    if not unique_docs:
        return "❌ No documents available to answer."

    llm = OpenAI(temperature=0)
    chain = load_qa_chain(llm, chain_type="stuff")
    answer = chain.run(input_documents=unique_docs, question=query)

    return answer
