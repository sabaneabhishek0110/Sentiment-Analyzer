from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import nltk
import matplotlib.pyplot as plt
import csv
import speech_recognition as sr
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

nrc_lexicon = {}
# Load the NRC Emotion Lexicon
with open('NRC-Emotion-Lexicon/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt', 'r') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        word, emotion, association = row
        if word not in nrc_lexicon:
            nrc_lexicon[word] = {}
        nrc_lexicon[word][emotion] = int(association)

class TextRequest(BaseModel):
    text: str

def calculate_sentiment_scores(emotions_count):
    """Calculate positive, negative, and neutral scores from NRC emotions"""
    # Positive contributors (with weights)
    positive_score = (
        emotions_count.get('positive', 0) * 1.0 + 
        emotions_count.get('joy', 0) * 0.8 +
        emotions_count.get('trust', 0) * 0.6 +
        emotions_count.get('surprise', 0) * 0.3  # Mildly positive
    )
    
    # Negative contributors (with weights)
    negative_score = (
        emotions_count.get('negative', 0) * 1.0 +
        emotions_count.get('anger', 0) * 0.9 +
        emotions_count.get('disgust', 0) * 0.7 +
        emotions_count.get('fear', 0) * 0.6 +
        emotions_count.get('sadness', 0) * 0.8
    )
    
    # Neutral base (anticipation is context-dependent)
    neutral_score = emotions_count.get('anticipation', 0) * 0.5
    
    # Normalize scores to percentages
    total = positive_score + negative_score + neutral_score + 1e-6  # Avoid division by zero
    return {
        "positive": round(positive_score / total * 100, 1),
        "negative": round(negative_score / total * 100, 1),
        "neutral": round(neutral_score / total * 100, 1)
    }

def determine_sentiment(scores):
    """Determine overall sentiment label"""
    if scores['positive'] > scores['negative'] + 10:  # 10% threshold
        return "positive"
    elif scores['negative'] > scores['positive'] + 10:
        return "negative"
    else:
        return "neutral"


@app.post("/analyze")
async def analyze_text(request : TextRequest):
    try:
        text = request.text
        lowercase = text.lower()
        cleaned_text = lowercase.translate(str.maketrans(" ", " ", string.punctuation))

        Tokenised_words = word_tokenize(cleaned_text, "english")

        final_words = []
        for word in Tokenised_words:
            if word not in stopwords.words("english"):
                final_words.append(word)


        # Initialize emotion counters
        emotions_count = {
            'anger': 0,
            'anticipation': 0,
            'disgust': 0,
            'fear': 0,
            'joy': 0,
            'sadness': 0,
            'surprise': 0,
            'trust': 0,
            'positive': 0,
            'negative': 0
        }

        # Analyze emotions in text
        for word in final_words:
            if word in nrc_lexicon:
                for emotion, association in nrc_lexicon[word].items():
                    if association == 1:
                        emotions_count[emotion] += 1

        w = Counter(emotions_count)
        print(w)

        # Vadar's Model
        # score = SentimentIntensityAnalyzer().polarity_scores(cleaned_text)
        # neg = score['neg']
        # pos = score['pos']
        # sentiment = "neutral"
        # print("negative : ",neg)
        # print("positive : ",pos)
        # if (pos > neg):
        #     sentiment = "positive"
        # elif (neg > pos):
        #     sentiment = "negative"

        sentiment_scores = calculate_sentiment_scores(emotions_count)
        sentiment = determine_sentiment(sentiment_scores)

        return {
            "success" : True,
            "emotions" : w,
            "sentiment" : sentiment,
            "sentiment_scores" : sentiment_scores
        }
    except Exception as e:
        print(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/speech_to_text")
async def speech_to_text():
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source2:
            print("Speech is Recognising.....")
            # Prepare Recognizer to recieve input
            r.adjust_for_ambient_noise(source2, duration=0.2)
            # Listen for users input
            audio2 = r.listen(source2)
            # Using google to recognize audio
            text = r.recognize_google(audio2)
            return {"success" : True,"text" : text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0",port=5000)

