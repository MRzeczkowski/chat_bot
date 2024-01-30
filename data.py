import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import json

import warnings
warnings.filterwarnings('ignore')


def load_data():
    with open('intents.json') as file:
        data = json.load(file)
    return data


def clean(line):
    cleaned_line = ''
    for char in line:
        if char.isalpha():
            cleaned_line += char
        else:
            cleaned_line += ' '
    cleaned_line = ' '.join(cleaned_line.split())
    return cleaned_line


def preprocess_data(data):
    intents = []

    text_input = []

    for intent in data['intents']:

        for text in intent['patterns']:
            text_input.append(clean(text))
            intents.append(intent['tag'])

    tokenizer = Tokenizer(filters='', oov_token='<unk>')
    tokenizer.fit_on_texts(text_input)
    sequences = tokenizer.texts_to_sequences(text_input)
    padded_sequences = pad_sequences(sequences, padding='pre')

    intent_to_index = {}
    categorical_target = []
    index = 0

    for intent in intents:
        if intent not in intent_to_index:
            intent_to_index[intent] = index
            index += 1
        categorical_target.append(intent_to_index[intent])

    num_classes = len(intent_to_index)

    # Convert intent_to_index to index_to_intent
    index_to_intent = {index: intent for intent,
                       index in intent_to_index.items()}

    categorical_vec = tf.keras.utils.to_categorical(categorical_target,
                                                    num_classes=num_classes, dtype='int32')

    return tokenizer.word_index, index_to_intent, padded_sequences, categorical_vec
