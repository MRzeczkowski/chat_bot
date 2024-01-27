import json
import string
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download("punkt")
nltk.download("wordnet")


def load_data():
    with open('intents.json') as file:
        data = json.load(file)
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
