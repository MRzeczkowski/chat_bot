from data import load_data, preprocess_data
from model import build_model, train_model
from predict import pred_class
from response import get_response
import numpy as np
import random
import nltk
from nltk.stem import WordNetLemmatizer


def create_training_data(words, classes, doc_X, doc_y):
    training = []
    out_empty = [0] * len(classes)

    for idx, doc in enumerate(doc_X):
        bow = []
        text_words = nltk.word_tokenize(doc)
        lemmatizer = WordNetLemmatizer()
        text_words = [lemmatizer.lemmatize(
            word.lower()) for word in text_words]
        for word in words:
            bow.append(1) if word in text_words else bow.append(0)

        output_row = list(out_empty)
        output_row[classes.index(doc_y[idx])] = 1
        training.append([bow, output_row])

    random.shuffle(training)
    training = np.array(training, dtype=object)
    train_X = np.array(list(training[:, 0]))
    train_y = np.array(list(training[:, 1]))

    return train_X, train_y


def main():
    data = load_data()
    words, classes, doc_X, doc_y = preprocess_data(data)
    train_X, train_y = create_training_data(words, classes, doc_X, doc_y)

    input_shape = (len(train_X[0]),)
    output_shape = len(train_y[0])
    model = build_model(input_shape, output_shape)
    model = train_model(model, train_X, train_y)

    print("Chatbot is running! Type 'quit' to exit.")
    while True:
        message = input("You: ")
        if message.lower() == "quit":
            break

        intents = pred_class(message, words, classes, model)
        if intents:
            result = get_response(intents, data)
            print("Bot:", result)
        else:
            print("Bot: I don't understand.")


if __name__ == "__main__":
    main()
