import os
import streamlit as st
from dotenv import load_dotenv
from langchain.vectorstores import Qdrant
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tempfile
import qdrant_client

# Load .env secrets
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize embeddings and Qdrant client
embeddings = OpenAIEmbeddings()
qdrant = qdrant_client.QdrantClient(host="localhost", port=6333)

st.set_page_config(page_title="Smart Doc Chatbot", layout="wide")
st.title("📄 Multi-Document Smart Chatbot")

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

# Upload section
uploaded_files = st.file_uploader("Upload PDF or Text files", type=["pdf", "txt"], accept_multiple_files=True)

if st.button("Index Files"):
    docs = []

    for file in uploaded_files:
        suffix = file.name.split('.')[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        if file.name.endswith(".pdf"):
            loader = PyPDFLoader(tmp_path)
        else:
            loader = TextLoader(tmp_path)

        loaded_docs = loader.load()
        docs.extend(loaded_docs)

    # Split documents
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    # Store in Qdrant
    st.session_state.vectorstore = Qdrant.from_documents(
        chunks,
        embeddings,
        url="http://localhost:6333",
        prefer_grpc=False,
        collection_name="smart-docs",
    )

    st.success(f"Indexed {len(chunks)} chunks to Qdrant!")

# Chat section
if st.session_state.vectorstore:
    query = st.text_input("Ask a question about your documents:")
    if query:
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=st.session_state.vectorstore.as_retriever(),
            chain_type="stuff",
            return_source_documents=True  # Telling LangChain to return sources
        )
        result = qa_chain(query)

        st.write("🤖", result["result"])

        # Show sources
        if result.get("source_documents"):
            st.markdown("#### 📚 Sources:")
            for doc in result["source_documents"]:
                source = doc.metadata.get("source", "Unknown")
                st.markdown(f"- `{source}`")
