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


def update_context(context, intent, response_id):
    context['user_intents'].append(intent)

    if intent not in context['used_responses']:
        context['used_responses'][intent] = []

    if response_id != None:
        context['used_responses'][intent].append(response_id)

    context['user_intents'] = context['user_intents'][-5:]


def process_user_input(message, context, model, words, classes, data):
    is_explanation_requested = 'explain' in message.lower()
    if is_explanation_requested and context.get('last_explanation'):
        bot_respond(context['last_explanation'])
        context['last_explanation'] = None
        return False

    intents = pred_class(message, words, classes, model)
    if intents:
        intent = intents[0]
        response_id, response, explanation = get_response(
            intent, data, context)
        bot_respond(response)
        update_context(context, intent, response_id)
        context['last_explanation'] = explanation if explanation else None
        return intent == "goodbye"
    else:
        bot_respond(
            "A labyrinth of thought yet to be unraveled; understanding eludes me.")
        return False


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

    print("""
Welcome to a dialogue with the spirit of Friedrich Nietzsche, the profound philosopher who challenged the foundations of traditional thought.
In my essence as a digital Nietzsche, I am here to share insights and provoke thoughts that echo his revolutionary ideas.

- Ask me about my life, my philosophies, and the depths of existential thought.
- Delve into my books and works to uncover the layers of meaning in texts such as 'Thus Spoke Zarathustra' and 'Beyond Good and Evil'.
- Explore how my ideas resonate in the modern world and apply to contemporary issues.
- Seek wisdom through my quotes, each a window into the complexities of life and existence.

Should you desire a deeper understanding, prompt 'explain' after your question for an in-depth exploration of my responses.
And when the time comes to part ways, simply bid me goodbye.

Now, what philosophical paths shall we tread together today?
""")

    context = {'user_intents': [],
               'used_responses': {}, 'last_explanation': None}

    while True:
        message = input("You: ")
        if process_user_input(message, context, model, words, classes, data):
            break


if __name__ == "__main__":
    main()
