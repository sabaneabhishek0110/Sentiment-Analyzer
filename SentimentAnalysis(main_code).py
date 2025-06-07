import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import matplotlib.pyplot as plt
import csv
import speech_recognition as sr
# import pyttsx3
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nrc_lexicon = {}
# Load the NRC Emotion Lexicon
with open('NRC-Emotion-Lexicon/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt', 'r') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        word, emotion, association = row
        if word not in nrc_lexicon:
            nrc_lexicon[word] = {}
        nrc_lexicon[word][emotion] = int(association)

print("Select Your Choice Below and Enter Accordingly: ")
print("Speech Recognition : 1")
print("From File : 2")
n = input("Your Choice : ")
if(n=='1'):
    # Initialize the recogniser
    r = sr.Recognizer()

    def input():
        # Loop in case of error
        # while(1):
        try:
            with sr.Microphone() as source2:
                print("Speech is Recognising.....")
                # Prepare Recognizer to recieve input
                r.adjust_for_ambient_noise(source2, duration=0.2)
                # Listen for users input
                audio2 = r.listen(source2)
                # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                return MyText

        except sr.RequestError as e:
            print("could not request results. {0}".format(e))
        except sr.UnknownValueError:
            print("Unknown erroor occured.")

        return

    def output(text):
        f = open("Output.txt", 'w')
        f.write(text)
        f.write("\n")
        f.close()
        return

    # while(1):
    text = input()
    if (text):
        output(text)
        print("speech recognised")
        text = open('Output.txt', encoding='UTF-8').read()
        lowercase = text.lower()
        cleaned_text = lowercase.translate(str.maketrans(" ", " ", string.punctuation))
        # print(string.punctuation) ----> This are all the punctuations can present in txt file
        # print(cleaned_text)

        # Tokenisation---->splitting the words of read.txt file and storing in the list
        # Tokenised_words = cleaned_text.split() ------->Take lot of time for long text file like book
        Tokenised_words = word_tokenize(cleaned_text,"english")
        # print(Tokenised_words)

        # Stopwords----->this are the words which are not useful or meainningful according to sentiment analysis like I,me,mine,he

        # stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours',
        #               'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself',
        #               'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself',
        #               'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
        #               'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is',
        #               'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
        #               'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
        #               'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during',
        #               'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
        #               'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
        #               'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
        #               'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
        #               'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're',
        #               've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn',
        #               "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma',
        #               'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn',
        #               "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

        final_words = []
        for word in Tokenised_words:
            if word not in stopwords.words("english"):
                final_words.append(word)
            # print(final_words)

            # Emotion Algorithm for sentiment analysis
            # emotion_list = []
            # with open('emotions.txt','r') as file :
            #     for line in file :
            #         clear_line = line.replace("\n",'').replace(",",'').replace("'",'').strip()
            #         # print(clear_line)
            #         word,emotion = clear_line.split(":")
            #         # print("Word : "+ word + "   " + "Emotion : " + emotion)
            #         if word in final_words :
            #             emotion_list.append(emotion)
            # print(emotion_list)

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

        def overall_sentiment_analysis(sentiment_text):
            score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
            neg = score['neg']
            pos = score['pos']
            if(pos>neg):
                print("Overall sentiment is Positive")
            elif(neg>pos):
                print("Overall sentiment is Negative")
            else:
                print("Overall sentiment is Neutral")

        overall_sentiment_analysis(cleaned_text)
        fig, ax1 = plt.subplots()
        ax1.bar(w.keys(), w.values())
        fig.autofmt_xdate()
        plt.savefig('graph.png')
        plt.show()
    else:
        print("speech is not recognized")

elif(n=='2'):
    # Removing all punctuations from text and making text lowercase
    text = open('Data/content.txt', encoding='UTF-8').read()

    lowercase = text.lower()
    cleaned_text = lowercase.translate(str.maketrans(" ", " ", string.punctuation))
    # print(string.punctuation) ----> This are all the punctuations can present in txt file
    # print(cleaned_text)

    # Tokenisation---->splitting the words of read.txt file and storing in the list
    # Tokenised_words = cleaned_text.split() ------->Take lot of time for long text file like book
    Tokenised_words = word_tokenize(cleaned_text, "english")
    # print(Tokenised_words)

    # Stopwords----->this are the words which are not useful or meainningful according to sentiment analysis like I,me,mine,he

    # stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours',
    #               'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself',
    #               'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself',
    #               'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
    #               'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is',
    #               'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
    #               'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
    #               'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during',
    #               'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
    #               'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
    #               'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
    #               'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
    #               'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're',
    #               've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn',
    #               "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma',
    #               'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn',
    #               "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

    final_words = []
    for word in Tokenised_words:
        if word not in stopwords.words("english"):
            final_words.append(word)
    # print(final_words)

    # Emotion Algorithm for sentiment analysis
    # emotion_list = []
    # with open('emotions.txt','r') as file :
    #     for line in file :
    #         clear_line = line.replace("\n",'').replace(",",'').replace("'",'').strip()
    #         # print(clear_line)
    #         word,emotion = clear_line.split(":")
    #         # print("Word : "+ word + "   " + "Emotion : " + emotion)
    #         if word in final_words :
    #             emotion_list.append(emotion)
    # print(emotion_list)

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


    def overall_sentiment_analysis(sentiment_text):
        score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
        neg = score['neg']
        pos = score['pos']
        if (pos > neg):
            print("Overall sentiment is Positive")
        elif (neg > pos):
            print("Overall sentiment is Negative")
        else:
            print("Overall sentiment is Neutral")


    overall_sentiment_analysis(cleaned_text)

    fig , ax1 = plt.subplots()
    ax1.bar(w.keys() , w.values())
    fig.autofmt_xdate()
    plt.savefig('graph.png')
    plt.show()

else:
    print("Invalid Choice. Please select Choice either 1 or 2.")