from fastapi import FastAPI 
from pydantic import BaseModel

app = FastAPI()

@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }
@app.get("/documents")
def get_documents():
    return {
        "documents": [
            "attendance-policy.txt"
        ]
    }

class QuestionRequest(BaseModel):
    question: str

@app.post("ask")
def ask_question(request: QuestionRequest):
    return {
        "question": request.question,
        "answer": "AI answer will go here later"
    }