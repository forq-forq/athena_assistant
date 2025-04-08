import streamlit as st
import uuid
from utils.document_loader import load_file
from utils.embedder import embed_documents, get_all_documents, delete_document_by_source
from langchain_core.documents import Document

def admin_ui():
    st.title("🛠️ Admin Panel")

    st.subheader("📥 Add document to database")
    files = st.file_uploader("Choose files", type=["pdf", "docx", "txt", "md"], accept_multiple_files=True)

    existing_docs = get_all_documents()
    existing_sources = set(doc.metadata.get("source") for doc in existing_docs)

    if st.button("➕ Add to database") and files:
        docs_to_embed = []
        skipped_files = []

        for file in files:
            try:
                text, filename = load_file(file)
                if filename in existing_sources:
                    skipped_files.append(filename)
                    continue

                doc = Document(
                    page_content=text,
                    metadata={
                        "id": str(uuid.uuid4()),
                        "source": filename
                    }
                )
                docs_to_embed.append(doc)
            except Exception as e:
                st.warning(f"❌ Processing error {file.name}: {e}")

        if docs_to_embed:
            embed_documents(docs_to_embed)
            st.success("✅ Documents have been successfully added to the database.")
            st.rerun()

        if skipped_files:
            st.info(f"ℹ️ The following files are already in the database and were skipped: {', '.join(skipped_files)}")

    st.divider()

    st.subheader("📚 Database")
    documents = get_all_documents()
    unique_sources = sorted(set(doc.metadata.get("source", "Unknown") for doc in documents))

    for source in unique_sources:
        with st.expander(f"📄 {source}"):
            text_preview = "\n".join(
                doc.page_content for doc in documents if doc.metadata.get("source") == source
            )
            st.text_area("Content", value=text_preview, height=200, key=f"text_{source}")

            with st.form(key=f"form_delete_{source}"):
                submit_delete = st.form_submit_button(f"🗑 Delete fail '{source}'")
                if submit_delete:
                    deleted = delete_document_by_source(source)
                    if deleted:
                        st.success(f"✅ File '{source}' has been deleted from database.")
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete file.")
