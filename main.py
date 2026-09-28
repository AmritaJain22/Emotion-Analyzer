import string
import joblib
import nltk

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from nltk.corpus import stopwords


# =====================================================
# PROJECT PATH
# =====================================================

BASE_DIR = Path(__file__).resolve().parent


# =====================================================
# STOPWORDS
# =====================================================

try:
    stop_words = set(stopwords.words("english"))

except LookupError:
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))


# =====================================================
# LOAD MODEL
# =====================================================

model = joblib.load(
    BASE_DIR / "model.pkl"
)


# =====================================================
# LOAD TF-IDF VECTORIZER
# =====================================================

tfidf_vectorizer = joblib.load(
    BASE_DIR / "tfidf_vectorizer.pkl"
)


# =====================================================
# FASTAPI
# =====================================================

app = FastAPI(
    title="Sentiment Analysis NLP",
    description="Emotion Classification using TF-IDF and Logistic Regression",
    version="1.0"
)


# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


# =====================================================
# INPUT MODEL
# =====================================================

class TextInput(BaseModel):

    text: str


# =====================================================
# PREPROCESSING
# Same as your notebook
# =====================================================

def preprocess_text(text):

    # Lowercase
    text = text.lower()

    # Remove punctuation
    text = text.translate(
        str.maketrans(
            "",
            "",
            string.punctuation
        )
    )

    # Remove stopwords
    words = text.split()

    cleaned_words = []

    for word in words:

        if word not in stop_words:

            cleaned_words.append(word)

    return " ".join(cleaned_words)


# =====================================================
# HOME
# =====================================================

@app.get("/")
def home():

    return FileResponse(
        BASE_DIR / "index.html"
    )


# =====================================================
# CSS
# =====================================================

@app.get("/style.css")
def style():

    return FileResponse(
        BASE_DIR / "style.css"
    )


# =====================================================
# JAVASCRIPT
# =====================================================

@app.get("/script.js")
def script():

    return FileResponse(
        BASE_DIR / "script.js"
    )


# =====================================================
# PREDICT
# =====================================================

@app.post("/predict")
def predict(data: TextInput):

    text = data.text.strip()

    if not text:

        return {
            "success": False,
            "message": "Please enter some text."
        }


    # Preprocess
    cleaned_text = preprocess_text(
        text
    )


    # TF-IDF
    text_vector = tfidf_vectorizer.transform(
        [cleaned_text]
    )


    # Prediction
    prediction = model.predict(
        text_vector
    )[0]


    # Confidence
    probabilities = model.predict_proba(
        text_vector
    )[0]

    confidence = max(
        probabilities
    ) * 100


    return {

        "success": True,

        "text": text,

        "cleaned_text": cleaned_text,

        "emotion": str(prediction),

        "confidence": round(
            confidence,
            2
        )
    }