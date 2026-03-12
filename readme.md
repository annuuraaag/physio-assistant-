# AI Physiotherapy Assistant (RAG + LangGraph)

An intelligent, safety-aware physiotherapy assistant built using Retrieval-Augmented Generation (RAG) and LangGraph orchestration.  
The system provides evidence-based rehabilitation guidance from physiotherapy documents while enforcing clinical safety rules and structured responses.

---

## Overview

This project demonstrates a production-style architecture for domain-specific conversational AI in healthcare.  
It combines document retrieval, large language models, conversational memory, and safety guardrails to deliver reliable guidance.

The assistant answers physiotherapy-related questions using a PDF knowledge base and supports multi-turn conversations while monitoring for risky symptoms.

---

## Key Features

- Knowledge-grounded answers from physiotherapy guidelines
- Semantic search using FAISS vector database
- LangGraph-based orchestration pipeline
- Intent classification for user queries
- Clinical safety guardrails (red-flag detection)
- Structured medical-safe responses
- Multi-turn conversation with memory
- OCR-based ingestion for scanned documents
- Streamlit chat interface
- FastAPI service layer (optional backend API)

---

## Architecture

### Processing Pipeline

User Query → Intent Classification → Document Retrieval → Safety Check → Response Generation → Memory Update

### Core Components

#### 1. Document Processing
- PDF ingestion with OCR (for scanned documents)
- Text extraction using Tesseract
- Text chunking via RecursiveCharacterTextSplitter

#### 2. Vector Database
- Embeddings: Sentence Transformers (all-MiniLM-L6-v2)
- Storage: FAISS local vector store
- Semantic similarity search

#### 3. LangGraph Workflow Nodes

- **Intent Classifier** — Identifies user goal (exercise guidance, pain explanation, rehab plan, safety warning)
- **Retriever** — Fetches relevant document chunks
- **Safety Guardrail** — Detects risky or diagnostic requests
- **Response Generator** — Produces structured answer using LLM
- **Memory Node** — Tracks conversation context across turns

#### 4. Clinical Safety Layer

The assistant enforces the following rules:

- Does not provide medical diagnosis
- Detects red-flag symptoms
- Provides precautions
- Recommends consulting a licensed physiotherapist
- Generates structured, responsible responses

---

## Technology Stack

- Python
- LangChain
- LangGraph
- FAISS
- Sentence Transformers
- Groq LLM API (LLaMA-based models)
- Tesseract OCR
- Streamlit (UI)
- FastAPI (API layer)
- python-dotenv

---

## Setup Instructions

### 1. Clone the Repository

git clone https://github.com/annuraaaag/physio-assistant-.git
cd physio-assistant-

### 2. Create Virtual Environment
Windows (PowerShell)
python -m venv venv
venv\Scripts\activate
macOS / Linux
python3 -m venv venv
source venv/bin/activate

### 3. Install Dependencies
pip install -r requirement.txt
### 4. Configure Environment Variables

Create a .env file in the project root:

GROQ_API_KEY=your_api_key_here
### 5. Add Knowledge Base Document

Place the physiotherapy PDF inside the docs/ folder.

Example:

docs/inputdata.pdf

### 6. Build Vector Database

Run the ingestion script:

python ingest.py

This will:

Extract text (including scanned PDFs)

Split text into chunks

Generate embeddings

Create FAISS index in faiss_index/

### 7. Run the Application
Streamlit Interface
streamlit run app.py
FastAPI Backend (Optional)
uvicorn api:app --reload

### Project Structure
physio-assistant/
│
├── app.py                 # Streamlit frontend
├── api.py                 # FastAPI backend service
├── rag_graph.py           # LangGraph workflow definition
├── ingest.py              # Document ingestion pipeline
├── faiss_index/           # Vector database files
├── docs/                  # Source PDF documents
├── requirement.txt        # Python dependencies
├── .env.example           # Environment variable template
├── test.py                # CLI testing script
└── README.md

### Example Use Cases

Exercise guidance for common injuries

Pain explanation and rehabilitation advice

Recovery stage assistance

Safety warnings for severe symptoms

Educational physiotherapy support

### Limitations

Not a substitute for professional medical advice

Dependent on the quality of the source documents

Does not perform diagnosis

Requires internet access for LLM API

### Future Improvements

Deployment on cloud infrastructure

Persistent conversation memory

Multi-document support

Voice interface integration

Clinical validation workflows

Authentication and user profiles

### Disclaimer

This assistant provides informational guidance only and is not intended to replace professional medical consultation.
Users should consult a licensed physiotherapist or healthcare provider for diagnosis and treatment.

### License

This project is for educational and demonstration purposes.
