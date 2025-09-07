# P3: Minimal local RAG-like retrieval with FastAPI (no external LLM)
import os, glob, json
from fastapi import FastAPI, Body
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title="P3 RAG Safety Copilot (Local Retrieval)")

CORPUS_DIR = os.environ.get("CORPUS_DIR","docs/corpus")
os.makedirs(CORPUS_DIR, exist_ok=True)

class Query(BaseModel):
    question: str
    top_k: int = 5

def load_corpus():
    docs, paths = [], []
    for p in glob.glob(os.path.join(CORPUS_DIR, "*.txt")):
        txt = open(p, encoding="utf-8").read()
        docs.append(txt); paths.append(os.path.basename(p))
    return docs, paths

docs, paths = load_corpus()
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(docs) if docs else None

@app.get("/health")
def health(): return {"status":"ok","docs":len(docs)}

@app.post("/ask")
def ask(q: Query):
    if X is None or len(docs)==0:
        return {"answer":"No corpus available. Please add SOPs/P&IDs/Incidents as .txt files.","sources":[],"advisory":True}
    v = vectorizer.transform([q.question])
    sims = cosine_similarity(v, X).ravel()
    idx = sims.argsort()[::-1][:q.top_k]
    sources = [{"doc": paths[i], "score": float(sims[i])} for i in idx]
    answer = "Advisory-only: Based on retrieved SOPs/P&IDs, consult operator and confirm before action."
    return {"answer":answer, "sources":sources, "advisory":True}
