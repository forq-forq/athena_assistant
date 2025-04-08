import streamlit as st
from utils.document_loader import load_file
from utils.embedder import get_all_documents
from utils.qa_chain import answer_question
from langchain_core.documents import Document

def user_ui():
    st.title("💡 Athena Knowledge Assistant")

    uploaded_files = st.file_uploader(
        "📎 Attach files for the request (not saved to the database)",
        type=["pdf", "docx", "txt", "md"],
        accept_multiple_files=True,
        key="user_file_upload"
    )

    session_docs = []
    if uploaded_files:
        for file in uploaded_files:
            try:
                text, filename = load_file(file)
                doc = Document(page_content=text, metadata={"source": filename})
                session_docs.append(doc)
            except Exception as e:
                st.warning(f"❌ Processing error {file.name}: {e}")

    st.divider()
    st.subheader("💬 Ask a question based on the database + attached files")
    query = st.text_input("Question:", key="user_question")

    if st.button("📨 Send request") and query:
        with st.spinner("🔍 Searching and generating an answer..."):
            try:
                db_docs = get_all_documents()
                all_docs = db_docs + session_docs if session_docs else db_docs
                response = answer_question(query, custom_documents=all_docs)
                st.markdown("### 🤖 Answer:")
                st.write(response)
            except Exception as e:
                st.error(f"⚠️ Request processing error: {str(e)}")
