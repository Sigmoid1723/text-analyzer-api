from fastapi import FastAPI
from pydantic import BaseModel
from collections import Counter
import re


app = FastAPI()


class TextInput(BaseModel):
    text: str

@app.get("/health/")
def health():
    return {"status": "ok", "version" : "1.0"}

@app.post("/analyze")
def analyze(payload: TextInput):
    text = payload.text
    words = re.findall(r'\b\w+\b',text.lower())
    sentences = [s.strip() for s in re.split(r'[.!?]',text) if s.strip()]
    top_words = Counter(words).most_common(5)

    return {
        "word_count" : len(words),
        "sentence_count" : len(sentences),
        "top_5_words": top_words
    }
