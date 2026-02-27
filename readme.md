# 🩺 AI Physiotherapy Assistant (RAG + LangGraph)

An intelligent, safety-aware physiotherapy assistant built using Retrieval-Augmented Generation (RAG) and LangGraph orchestration.
The system provides evidence-based rehabilitation guidance using physiotherapy documents while enforcing clinical safety rules.

---

## 🚀 Features

* 📄 Knowledge-based answers from physiotherapy guidelines (PDF)
* 🧠 Semantic search using FAISS vector database
* 🔁 Multi-turn conversation with memory
* 🛡️ Clinical safety guardrails (red-flag detection)
* 🧩 Intent classification for user queries
* 📋 Structured medical-safe responses
* 💬 Chat interface built with Streamlit
* ⚡ Powered by Groq LLM

---

## 🏗️ Architecture Overview

User → Intent Classification → Retrieval → Safety Check → Response Generation → Memory Update

### Core Components

**1. Document Processing**

* PDF ingestion with OCR (for scanned documents)
* Text chunking using RecursiveCharacterTextSplitter

**2. Vector Database**

* Embeddings: Sentence Transformers (all-MiniLM-L6-v2)
* Storage: FAISS (local vector store)

**3. LangGraph Workflow**

Nodes:

* Intent Classifier — Understands user goal
* Retriever — Semantic search from knowledge base
* Safety Guardrail — Detects risky symptoms
* Response Generator — Creates structured answer
* Memory Node — Tracks conversation context

**4. Clinical Safety Rules**

The assistant:

* Never provides diagnosis
* Detects red-flag symptoms
* Advises consulting a licensed physiotherapist
* Provides precautions and escalation guidance

---

## 🖥️ Tech Stack

* Python
* LangChain
* LangGraph
* FAISS
* Sentence Transformers
* Groq LLM API
* Streamlit
* pytesseract (OCR)
* pdf2image

---

## 📁 Project Structure

```
physio_assistant/
│
├── docs/                  # Input PDF files
├── faiss_index/           # Vector database (generated)
├── ingest.py              # Builds FAISS index
├── rag_graph.py           # LangGraph pipeline
├── app.py                 # Streamlit UI
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone <your-repo-url>
cd physio_assistant
```

---

### 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

---

### 5. Add physiotherapy PDF

Place your document inside the `docs/` folder.

---

### 6. Build vector database

```
python ingest.py
```

This creates the FAISS index.

---

### 7. Run the application

```
streamlit run app.py
```

---

## 💬 Example Queries

* “Knee pain after running”
* “Exercises for shoulder stiffness”
* “Lower back pain relief”
* “Pain when climbing stairs”

---

## ⚠️ Disclaimer

This assistant provides educational guidance only and is not a substitute for professional medical advice.

Always consult a licensed physiotherapist for diagnosis and treatment.

---

## 📦 Deployment

The application can be deployed using Streamlit Cloud.

---

## 👨‍💻 Author

Anurag Mazumdar
AI / Software Engineering Graduate

---

## 📄 License

For educational and demonstration purposes.
