from rag_graph import run_assistant

question = input("Ask a physiotherapy question: ")
answer = run_assistant(question)

print("\nAssistant:", answer)