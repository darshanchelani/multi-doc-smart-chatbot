# 📄 Multi-Document Smart Retrieval Chatbot

An AI-powered Streamlit application that allows users to upload multiple documents (PDF or TXT), index them into a vector database (Qdrant), and ask questions in natural language. The chatbot retrieves the most relevant information using OpenAI and LangChain — with sources cited!

---

### 🚀 Features

- Upload and index multiple PDF/TXT documents
- Semantic search using OpenAI embeddings
- Q&A with context-aware responses
- Source citation for transparency
- Dockerized backend with Qdrant integration

---

### 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python, LangChain, OpenAI
- **Vector Store**: Qdrant
- **Document Processing**: PyPDFLoader, TextLoader
- **Deployment**: Docker, Docker Compose

---

### 📦 Installation

```bash
git clone https://github.com/darshanchelani/multi-doc-smart-chatbot
cd multi-doc-smart-chatbot
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_key
QDRANT_URL=http://localhost:6333
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start Qdrant with Docker:

```bash
docker-compose up -d
```

Run the Streamlit app:

```bash
streamlit run app.py
```

---

### 🐳 Docker Setup (Optional)

To run everything in Docker:

```bash
docker build -t multi-doc-chatbot .
docker run -p 8501:8501 --env-file .env multi-doc-chatbot
```

---

### 📷 Preview

![screenshot](Screenshot/ss.png)

---

### 🧠 Powered By

- [LangChain](https://www.langchain.com/)
- [OpenAI](https://platform.openai.com/)
- [Qdrant](https://qdrant.tech/)
- [Streamlit](https://streamlit.io/)

---

## Contribution

Feel free to fork the repository and submit a pull request. Contributions are welcome!