import speech_recognition as sr
import pyttsx3

# Initialize the recogniser
r = sr.Recognizer()

def input():
    #Loop in case of error
    # while(1):
    try :
        with sr.Microphone() as source2 :
         # Prepare Recognizer to recieve input
            r.adjust_for_ambient_noise(source2,duration = 0.2)
         #Listen for users input
            audio2 = r.listen(source2)
         #Using google to recognize audio
            MyText = r.recognize_google(audio2)
            return MyText

    except sr.RequestError as e :
        print("could not request results. {0}".format(e))
    except sr.UnknownValueError :
        print("Unknown erroor occured.")

    return

def output(text):
    f = open("Output.txt",'a')
    f.write(text)
    f.write("\n")
    f.close()
    return

# while(1):
text = input()
if(text):
    output(text)
    print("speech recognised")
else:
    print("speech is not recognized")