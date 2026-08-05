from fastapi import FastAPI
from pydantic import BaseModel
from collections import Counter
import re
from groq import Groq,APIError
import os
from dotenv import load_dotenv
from prompt_loader import load_prompts

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

prompts = load_prompts()

class TextInput(BaseModel):
    text: str

@app.get("/health")
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

@app.post("/summarize")
def summarize(payload: TextInput):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system","content": prompts["summarizer"]},
                {"role": "user","content":payload.text}
            ],
        )
        return {"summary": response.choices[0].message.content}
    except APIError as e:
        return {"API error occurred": str(e)}
    except Exception as e:
        return {"Unexpected error": str(e)}
