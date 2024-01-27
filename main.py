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


def bot_respond(response):
    print("Nietzsche bot:", response)


def main():
    data = load_data()
    words, classes, doc_X, doc_y = preprocess_data(data)
    train_X, train_y = create_training_data(words, classes, doc_X, doc_y)

    input_shape = (len(train_X[0]),)
    output_shape = len(train_y[0])
    model = build_model(input_shape, output_shape)
    model = train_model(model, train_X, train_y)

    bot_name = '''
    888b      88 88                                                   88                        88                              
    8888b     88 ""              ,d                                   88                        88                       ,d     
    88 `8b    88                 88                                   88                        88                       88     
    88  `8b   88 88  ,adPPYba, MM88MMM 888888888 ,adPPYba,  ,adPPYba, 88,dPPYba,   ,adPPYba,    88,dPPYba,   ,adPPYba, MM88MMM  
    88   `8b  88 88 a8P_____88   88         a8P" I8[    "" a8"     "" 88P'    "8a a8P_____88    88P'    "8a a8"     "8a  88     
    88    `8b 88 88 8PP"""""""   88      ,d8P'    `"Y8ba,  8b         88       88 8PP"""""""    88       d8 8b       d8  88     
    88     `8888 88 "8b,   ,aa   88,   ,d8"      aa    ]8I "8a,   ,aa 88       88 "8b,   ,aa    88b,   ,a8" "8a,   ,a8"  88,    
    88      `888 88  `"Ybbd8"'   "Y888 888888888 `"YbbdP"'  `"Ybbd8"' 88       88  `"Ybbd8"'    8Y"Ybbd8"'   `"YbbdP"'   "Y888  
'''

    print(bot_name)
    print("Nietzsche bot is running! To exit simply say goodby to the bot. Prompt 'explain' after your question for an explanation - if there is one.\n")
    last_explanation = None

    while True:
        message = input("You: ")

        is_explanation_requested = 'explain' in message.lower()

        if is_explanation_requested and last_explanation:
            bot_respond(last_explanation)
            last_explanation = None
            continue

        intents = pred_class(message, words, classes, model)
        if intents:
            response, explanation = get_response(intents, data)
            bot_respond(response)

            if "goodbye" in intents:
                break  # Exit the chatbot

            last_explanation = explanation if explanation else None
        else:
            bot_respond(
                "A labyrinth of thought yet to be unraveled; understanding eludes me.")


if __name__ == "__main__":
    main()
