from fastapi import FastAPI
from pydantic import BaseModel
import os
import glob
import pathlib
import re
from typing import List, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = FastAPI(title="RAG Safety Co-Pilot")

# Build corpus at startup
CORPUS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "corpus")
documents: List[str] = []
doc_names: List[str] = []
vectorizer = TfidfVectorizer(stop_words="english")
doc_matrix = None


def load_corpus():
    global documents, doc_names, doc_matrix
    documents = []
    doc_names = []
    for path in glob.glob(os.path.join(CORPUS_DIR, "*")):
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            documents.append(content)
            doc_names.append(os.path.basename(path))
    if documents:
        doc_matrix = vectorizer.fit_transform(documents)
    else:
        doc_matrix = None


def retrieve(query: str, top_k: int = 2) -> List[Tuple[str, str]]:
    """
    Return top_k (content, name) pairs for the query.
    """
    if not documents or doc_matrix is None:
        return []
    q_vec = vectorizer.transform([query])
    sims = cosine_similarity(q_vec, doc_matrix).flatten()
    indices = np.argsort(sims)[::-1][:top_k]
    return [(documents[i], doc_names[i]) for i in indices]


class Question(BaseModel):
    question: str


@app.on_event("startup")
def startup_event():
    load_corpus()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(question: Question):
    """
    Retrieve relevant snippets and return a simple answer with citations and a confirmation request.
    """
    query = question.question.strip()
    if not query:
        return {"answer": "Please provide a non-empty question."}

    results = retrieve(query, top_k=2)
    if not results:
        return {"answer": "No documents found. Please populate the docs/corpus directory."}

    # Compose a simple answer: return the first two sentences from each retrieved document
    snippets = []
    citations = []
    for text, name in results:
        # naive sentence splitting
        sentences = re.split(r"(?<=[.!?])\s+", text)
        snippet = " ".join(sentences[:2]).strip()
        snippets.append(snippet)
        citations.append(name)

    answer = " ".join(snippets)
    answer += " [Sources: " + ", ".join(citations) + "]"
    answer += " — Please confirm this information with the control room before taking any action."

    return {"answer": answer}