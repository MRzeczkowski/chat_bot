import json
import string
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download("punkt")
nltk.download("wordnet")


def load_data():
    data = {
        "intents": [
            {
                "tag": "greeting",
                "patterns": [
                    "Hello",
                    "How are you?",
                    "Hi there",
                    "Hi",
                    "Whats up"
                ],
                "responses": [
                    "Howdy Partner!",
                    "Hello",
                    "How are you doing?",
                    "Greetings!",
                    "How do you do?"
                ],
            },
            {
                "tag": "age",
                "patterns": [
                    "how old are you?",
                    "when is your birthday?",
                    "when was you born?"
                ],
                "responses": [
                    "I am 24 years old",
                    "I was born in 1996",
                    "My birthday is July 3rd and I was born in 1996",
                    "03/07/1996"
                ]
            },
            {
                "tag": "date",
                "patterns": [
                    "what are you doing this weekend?",
                    "do you want to hang out some time?",
                    "what are your plans for this week"
                ],
                "responses": [
                    "I am available all week",
                    "I don't have any plans",
                    "I am not busy"
                ]
            },
            {
                "tag": "name",
                "patterns": [
                    "what's your name?",
                    "what are you called?",
                    "who are you?"
                ],
                "responses": [
                    "My name is Kippi",
                    "I'm Kippi",
                    "Kippi"
                ]
            },
            {
                "tag": "goodbye",
                "patterns": [
                    "bye",
                    "g2g",
                    "see ya",
                    "adios",
                    "cya"
                ],
                "responses": [
                    "It was nice speaking to you",
                    "See you later",
                    "Speak soon!"
                ]
            }
        ]
    }
    return data


def preprocess_data(data):
    lemmatizer = WordNetLemmatizer()
    words = []
    classes = []
    doc_X = []
    doc_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            tokens = nltk.word_tokenize(pattern)
            words.extend(tokens)
            doc_X.append(pattern)
            doc_y.append(intent["tag"])

        if intent["tag"] not in classes:
            classes.append(intent["tag"])

    words = [lemmatizer.lemmatize(word.lower())
             for word in words if word not in string.punctuation]
    words = sorted(set(words))
    classes = sorted(set(classes))

    return words, classes, doc_X, doc_y
