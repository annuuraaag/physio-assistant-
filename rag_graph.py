from dotenv import load_dotenv
import os

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

from langgraph.graph import StateGraph
from typing import TypedDict, List

# ---------- Load ENV ----------
load_dotenv()

# ---------- Load FAISS ----------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever()

# ---------- LLM ----------
llm = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0
)

# ---------- STATE ----------
class State(TypedDict):
    question: str
    context: str
    answer: str
    history: List[str]
    intent: str
    pain_location: str


# =========================================================
# 🔹 INTENT CLASSIFIER NODE (Phase 2)
# =========================================================
def intent_node(state: State):

    prompt = f"""
Classify the user intent into ONE of:

- exercise_guidance
- pain_explanation
- rehab_plan
- safety_warning
- general

User query:
{state['question']}

Return ONLY the label.
"""

    result = llm.invoke(prompt).content.strip().lower()

    return {"intent": result}


# =========================================================
# 🔹 RETRIEVAL NODE (RAG)
# =========================================================
def retrieve_node(state: State):

    docs = retriever.invoke(state["question"])
    context = "\n".join([doc.page_content for doc in docs])

    # Observability (Phase 5)
    print("Retrieved context preview:")
    print(context[:300])

    return {"context": context}


# =========================================================
# 🔹 SAFETY NODE (Phase 3)
# =========================================================
RED_FLAGS = [
    "severe swelling",
    "numbness",
    "tingling",
    "loss of movement",
    "fracture",
    "unable to walk",
    "acute injury"
]

def safety_node(state: State):

    q = state["question"].lower()

    for flag in RED_FLAGS:
        if flag in q:
            return {
                "answer":
                "⚠️ This may indicate a serious condition. "
                "Please consult a licensed physiotherapist immediately."
            }

    return {}


# =========================================================
# 🔹 GENERATION NODE (Structured Medical Response)
# =========================================================
def generate_node(state: State):

    if not state.get("context", "").strip():
        return {
            "answer":
            "Information not available in the physiotherapy guidelines."
        }

    prompt = f"""
You are a physiotherapy assistant.

Use ONLY the provided context.

Provide response in this format:

Condition Explanation:
Recommended Exercises:
Precautions:
When to Seek Medical Help:

Always advise consulting a licensed physiotherapist.

Context:
{state['context']}

Question:
{state['question']}
"""

    response = llm.invoke(prompt)

    return {"answer": response.content}


# =========================================================
# 🔹 MEMORY NODE (Phase 4)
# =========================================================
def memory_node(state: State):

    q = state["question"].lower()

    if "knee" in q:
        location = "knee"
    elif "back" in q:
        location = "back"
    elif "neck" in q:
        location = "neck"
    else:
        location = state.get("pain_location", "unknown")

    history = state.get("history", [])
    history.append(q)

    return {
        "history": history,
        "pain_location": location
    }


# =========================================================
# 🔹 BUILD GRAPH (Phase 2 Architecture)
# =========================================================
graph = StateGraph(State)

graph.add_node("intent", intent_node)
graph.add_node("retrieve", retrieve_node)
graph.add_node("safety", safety_node)
graph.add_node("generate", generate_node)
graph.add_node("memory", memory_node)

graph.set_entry_point("intent")

graph.add_edge("intent", "retrieve")
graph.add_edge("retrieve", "safety")
graph.add_edge("safety", "generate")
graph.add_edge("generate", "memory")

app = graph.compile()


# =========================================================
# 🔹 PUBLIC FUNCTION
# =========================================================
chat_history = []

def run_assistant(question):

    global chat_history

    result = app.invoke({
        "question": question,
        "context": "",
        "answer": "",
        "history": chat_history,
        "intent": "",
        "pain_location": ""
    })

    chat_history = result.get("history", chat_history)

    return result["answer"]