import sys
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import matplotlib.pyplot as plt
import csv
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def load_nrc_lexicon():
    nrc_lexicon = {}
    with open('NRC-Emotion-Lexicon/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt', 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            word, emotion, association = row
            if word not in nrc_lexicon:
                nrc_lexicon[word] = {}
            nrc_lexicon[word][emotion] = int(association)
    return nrc_lexicon

def analyze_text(text, nrc_lexicon):
    lowercase = text.lower()
    cleaned_text = lowercase.translate(str.maketrans("", "", string.punctuation))
    tokenized_words = word_tokenize(cleaned_text, "english")
    final_words = [word for word in tokenized_words if word not in stopwords.words("english")]

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

    for word in final_words:
        if word in nrc_lexicon:
            for emotion, association in nrc_lexicon[word].items():
                if association == 1:
                    emotions_count[emotion] += 1

    return emotions_count, cleaned_text

def overall_sentiment_analysis(sentiment_text):
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    if score['pos'] > score['neg']:
        overall_sentiment = "Positive"
    elif score['neg'] > score['pos']:
        overall_sentiment = "Negative"
    else:
        overall_sentiment = "Neutral"
    return overall_sentiment

def save_graph(emotions_count, output_path):
    fig, ax1 = plt.subplots()
    ax1.bar(emotions_count.keys(), emotions_count.values())
    fig.autofmt_xdate()
    plt.savefig(output_path)

if __name__ == "__main__":
    input_text = sys.argv[1]
    nrc_lexicon = load_nrc_lexicon()
    emotions_count, cleaned_text = analyze_text(input_text, nrc_lexicon)
    overall_sentiment = overall_sentiment_analysis(cleaned_text)
    save_graph(emotions_count, 'graph.png')
    result = {
        'emotions_count': emotions_count,
        'overall_sentiment': overall_sentiment
    }
    print(result)
