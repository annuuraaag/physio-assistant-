from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# ---------- 1. Load PDF (OCR) ----------

import pytesseract
from pdf2image import convert_from_path
from langchain_core.documents import Document

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pdf_path = r"C:/Users/HP/OneDrive/Desktop/physio_assistant/docs/inputdata.pdf"

pages = convert_from_path(
    pdf_path,
    poppler_path=r"C:\poppler-25.12.0\Library\bin"
)

documents = []

for page in pages:
    text = pytesseract.image_to_string(page)

    #  CLEAN OCR TEXT (CRITICAL)
    text = text.replace("\n", " ")
    text = " ".join(text.split())

    #  Skip useless pages
    if len(text) > 80:
        documents.append(Document(page_content=text))

print("Extracted pages:", len(documents))


# ---------- 2. Chunk Text (LARGER CHUNKS) ----------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=900,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

# Remove tiny chunks
chunks = [c for c in chunks if len(c.page_content) > 100]

print("Total chunks:", len(chunks))


# ---------- 3. Create Embeddings ----------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ---------- 4. Store in FAISS ----------

vectorstore = FAISS.from_documents(chunks, embeddings)

vectorstore.save_local("faiss_index")

print(" FAISS index created successfully!")