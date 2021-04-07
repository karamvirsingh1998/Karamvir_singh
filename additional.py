import io
import random

import string # to process standard python strings
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
from tkinter import *
import pyttsx3 as pp
engine = pp.init()
voices=engine.getProperty('voices')
print(voices)
engine.setProperty('voice',voices[1].id)
def speak(word):
    engine.say(word)
    engine.runAndWait()

warnings.filterwarnings('ignore')


import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True) # for downloading packages

# uncomment the following only the first time
#nltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only


#Reading in the corpus
with open('file2.txt','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()

#TOkenisation
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences
word_tokens = nltk.word_tokenize(raw)# converts to list of words

# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Keyword Matching
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# Generating response
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

def get_response1(user_response):
    #print("ROBO: My name is Robo. I will answer your queries about Chatbots. If you want to exit, type Bye!")
        user_response=user_response.lower()
        if(user_response!='bye'):
          if(user_response=='thanks' or user_response=='thank you' ):
            return 'your welcome'
          else:
            if(greeting(user_response)!=None):
               return greeting(user_response)
            else:
               answer = response(user_response)
               sent_tokens.remove(user_response)
               return answer

        else:
          return 'BYE'

main = Tk()
main.geometry("500x650")
#500 is width and 650 is height
main.config(bg = "blue")
main.title("Xpertbot")
img =PhotoImage(file="chatbot1111.png") #img is object of class PhotoImage
photoL = Label(main,image=img,fg="pink", bg="black")
photoL.pack(pady=5) #yaxis pading=5

def ask_from_bot():
 user_response = textF.get()
 answer_from_bot = get_response1(user_response)
 msgs.insert(END,"you :" +user_response)
# sent_tokens.remove(user_response)
 msgs.insert(END,"Xpertbot : "+answer_from_bot)
 speak(answer_from_bot)
 textF.delete(0,END)
 msgs.yview(END)


frame =Frame(main) #list window for

sc = Scrollbar(frame)
msgs =Listbox(frame,width=80,height=20,yscrollcommand=sc.set)
sc.pack(side =RIGHT ,fill = Y)

#appear on right side
msgs.pack(side = LEFT ,fill =BOTH,pady=10)
frame.pack()

#creating text field
textF=Entry(main,font=("Verdana",20))
textF.pack(fill = X,pady=10)
btn =Button(main,text="Ask From XpertBot",font=("Verdana",20),command=ask_from_bot )
btn.pack()

def enter_function(event):
  btn.invoke()

#going to bind main window with eneter key
main.bind('<Return>',enter_function)

main.mainloop()
