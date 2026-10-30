from fastapi import FastAPI 
from pydantic import BaseModel
from retrieval import search_documents, load_documents

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }

@app.get("/documents")
def get_documents():
    documents = load_documents()
    return {
        "documents": [
            document["source"]
            for document in documents
        ]
    }

@app.post("/ask")
def ask_question(request: QuestionRequest):
    result = search_documents(request.question)
    return {
        "question": request.question,
        "source": result["source"],
        "context": result["context"],
        "score": result["score"]
    }