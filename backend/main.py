from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pythainlp.tokenize import word_tokenize
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str

class TextCountResult(BaseModel):
    total_words: int
    total_chars: int
    all_total_chars: int

def count_text(text: str) -> dict:
    thai_words = word_tokenize(text, engine='newmm', keep_whitespace=False)
    thai_words = [word for word in thai_words if word.strip() and re.search(r'[ก-๙]', word)]
    thai_chars = re.findall(r'[ก-๙]', text)

    english_words = re.findall(r'[a-zA-Z]+', text)
    english_chars = re.findall(r'[a-zA-Z]', text)

    total_words = len(thai_words) + len(english_words)
    total_chars = len(thai_chars) + len(english_chars)
    all_total_chars = len(text)

    return {
        "total_words": total_words,
        "total_chars": total_chars,
        "all_total_chars": all_total_chars
    }

@app.get("/")
def read_root():
    return {"message": "Text Analysis API"}

@app.post("/count-text", response_model=TextCountResult)
def reslut_count_text(input_data: TextInput):
    result = count_text(input_data.text)
    return TextCountResult(**result)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)