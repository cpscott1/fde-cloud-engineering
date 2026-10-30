import os
from pathlib import Path

# Default to the knowledge folder next to this file.
# Setting B2D_KNOWLEDGE_DIR overrides it (for example on a server or in Docker).
DEFAULT_KNOWLEDGE_DIR = Path(__file__).parent / "knowledge"
configured_directory = os.getenv("B2D_KNOWLEDGE_DIR")
knowledge_dir = Path(configured_directory) if configured_directory else DEFAULT_KNOWLEDGE_DIR


def load_documents():
    documents = []

    for file_path in knowledge_dir.glob("*.txt"):
        content = file_path.read_text(encoding="utf-8")

        document = {
            "source": file_path.name,
            "content": content
        }

        documents.append(document)

    return documents


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "can",
    "do",
    "for",
    "how",
    "i",
    "is",
    "of",
    "the",
    "to",
    "what",
    "when",
    "where"
}

def tokenize(text):
    cleaned_text = text.lower()
    for character in ",.?;:!":
        cleaned_text = cleaned_text.replace(character, "")
    useful_words = set(cleaned_text.split()) - STOP_WORDS
    return useful_words


def search_documents(question):
    question_words = tokenize(question)
    documents = load_documents()
    best_document = None
    best_score = 0
    for document in documents:
        document_words = tokenize(document["content"])
        matching_words = question_words.intersection(document_words)
        score = len(matching_words)
        if score > best_score:
            best_score = score
            best_document = document
    if best_document is None:
        return {
            "source": None,
            "context": None,
            "score": 0
        }
    return {
        "source": best_document["source"],
        "context": best_document["content"],
        "score": best_score
    }


if __name__ == "__main__":
    # Test prints and sample searches: these run only with `python3 retrieval.py`,
    # not when app.py imports this file.
    print(configured_directory)
    print(knowledge_dir)
    print(knowledge_dir.exists())

    print(load_documents())

    print(tokenize("What is the attendance policy"))

    result = search_documents("What is for lunch tommorow?")
    print(result)
