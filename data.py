import json
import string
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk

# Download necessary NLTK data
nltk.download("punkt")
nltk.download("wordnet")
nltk.download('stopwords')


def load_data():
    with open('intents.json') as file:
        data = json.load(file)
    return data


def preprocess_data(data):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    words = []
    classes = []
    doc_X = []
    doc_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            tokens = nltk.word_tokenize(pattern)
            words.extend([lemmatizer.lemmatize(word.lower(
            )) for word in tokens if word not in string.punctuation and word.lower() not in stop_words])
            doc_X.append(pattern)
            doc_y.append(intent["tag"])

        if intent["tag"] not in classes:
            classes.append(intent["tag"])

    words = sorted(set(words))
    classes = sorted(set(classes))

    return words, classes, doc_X, doc_y
