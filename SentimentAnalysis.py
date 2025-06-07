import sys
import string
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import matplotlib.pyplot as plt
import csv
import speech_recognition as sr
# import pyttsx3
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('vader_lexicon')

nrc_lexicon = {}
# Load the NRC Emotion Lexicon
with open('D:/Sentiment Analysis/NRC-Emotion-Lexicon/NRC-Emotion-Lexicon/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt', 'r') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        word, emotion, association = row
        if word not in nrc_lexicon:
            nrc_lexicon[word] = {}
        nrc_lexicon[word][emotion] = int(association)

def text_analyze(text) :
    lowercase = text.lower()
    cleaned_text = lowercase.translate(str.maketrans(" ", " ", string.punctuation))
    
    Tokenised_words = word_tokenize(cleaned_text,"english")
    final_words = []
    for word in Tokenised_words:
        if word not in stopwords.words("english"):
            final_words.append(word)
        
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

    w = emotions_count
    # print(json.dumps(w))
    # print(emotions_count)

    score = SentimentIntensityAnalyzer().polarity_scores(cleaned_text)
    neg = score['neg']
    pos = score['pos']
    if(pos>neg):
        Overall_sentiment = "Positive"
    elif(neg>pos):
        Overall_sentiment = "Negative"
    else:
        Overall_sentiment = "Neutral"

    # overall_sentiment_analysis(cleaned_text)
    # fig, ax1 = plt.subplots()
    # ax1.bar(w.keys(), w.values())
    # fig.autofmt_xdate()
    # plt.savefig('graph.png')
    # plt.show()

    return {
        # 'emotions_count': emotions_count,
        'emotion_distribution': dict(w),
        'overall_sentiment': Overall_sentiment
    }

def speech_recognize():
    r = sr.Recognizer()
    with sr.Microphone() as source2:
        print("Speech is Recognising.....")
        # Prepare Recognizer to recieve input
        r.adjust_for_ambient_noise(source2, duration=0.2)
        # Listen for users input
        audio2 = r.listen(source2)
        # Using google to recognize audio
        try:
            MyText = r.recognize_google(audio2)
            return MyText

        except sr.RequestError as e:
            print("could not request results. {0}".format(e))
        except sr.UnknownValueError:
            print("Unknown erroor occured.")

        return None

n='2'
def main():
    # print("Select Your Choice Below and Enter Accordingly: ")
    # print("Speech Recognition : 1")
    # print("From File : 2")
    # n = input("Your Choice : ")
    # n=sys.argv[2]
    # n = sys.argv[0]
    if(n=='1'):
        # Initialize the recogniser
        
        text = speech_recognize()
        def output(text):
            f = open("Data/Output.txt", 'w')
            f.write(text)
            f.write("\n")
            f.close()
            return

        # # while(1):
        text = input()
        if (text):
            output(text)
            print("speech recognised")
            text = open('Output.txt', encoding='UTF-8').read()
            result = text_analyze(text)
            print(json.dumps(result))
            

            # overall_sentiment_analysis(cleaned_text)
            # fig, ax1 = plt.subplots()
            # ax1.bar(w.keys(), w.values())
            # fig.autofmt_xdate()
            # plt.savefig('graph.png')
            # plt.show()\
            # plt.close(fig)
        else:
            print("speech is not recognized")

    elif(n=='2'):
        # Removing all punctuations from text and making text lowercase
        text = open('../Sentiment Analysis/Data/content.txt', encoding='UTF-8').read()
        result = text_analyze(text)
        print(json.dumps(result))

        # lowercase = text.lower()
        # cleaned_text = lowercase.translate(str.maketrans(" ", " ", string.punctuation))
        
        # Tokenised_words = word_tokenize(cleaned_text, "english")
        
        # final_words = []
        # for word in Tokenised_words:
        #     if word not in stopwords.words("english"):
        #         final_words.append(word)
        
        # # Initialize emotion counters
        #     emotions_count = {
        #         'anger': 0,
        #         'anticipation': 0,
        #         'disgust': 0,
        #         'fear': 0,
        #         'joy': 0,
        #         'sadness': 0,
        #         'surprise': 0,
        #         'trust': 0,
        #         'positive': 0,
        #         'negative': 0
        #     }

        # # Analyze emotions in text
        # for word in final_words:
        #     if word in nrc_lexicon:
        #         for emotion, association in nrc_lexicon[word].items():
        #             if association == 1:
        #                 emotions_count[emotion] += 1

        # w = Counter(emotions_count)
        # print(w)


        # def overall_sentiment_analysis(sentiment_text):
        #     score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
        #     neg = score['neg']
        #     pos = score['pos']
        #     if (pos > neg):
        #         print("Overall sentiment is Positive")
        #     elif (neg > pos):
        #         print("Overall sentiment is Negative")
        #     else:
        #         print("Overall sentiment is Neutral")


        # overall_sentiment_analysis(cleaned_text)

        # fig , ax1 = plt.subplots()
        # ax1.bar(w.keys() , w.values())
        # fig.autofmt_xdate()
        # plt.savefig('graph.png')
        # plt.show()

    else:
        print("Invalid Choice. Please select Choice either 1 or 2.")

    # result = {
    #         'emotions_count': emotions_count
    #     }
    # print(json.dumps(result))

if(__name__=="__main__"):
    main()