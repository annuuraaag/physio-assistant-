from fastapi import FastAPI
from pydantic import BaseModel
from rag_graph import run_assistant

app = FastAPI(title="Physiotherapy Assistant")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    return {"response": run_assistant(req.message)}