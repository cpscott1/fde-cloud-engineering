from fastapi import FastAPI 
from fastapi.responses import JSONResponse
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

@app.get("/ready")
def ready(): 
    documents = load_documents()
    document_count = len(documents)

    if document_count == 0:
        return JSONResponse(
            status_code=503,
            content={
                 "status": "not_ready",
                "document_count": 0
            }
        )
    
    return {
        "status": "ready",
        "document_count": document_count
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