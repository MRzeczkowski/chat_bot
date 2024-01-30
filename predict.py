import tensorflow as tf
import numpy as np


def pred_class(message, word_index, model):
    sent_tokens = []

    words = message.split()

    for word in words:

        if word in word_index:
            sent_tokens.append(word_index[word])
        else:
            sent_tokens.append(word_index['<unk>'])

    sent_tokens = tf.expand_dims(sent_tokens, 0)

    result = model.predict(sent_tokens, verbose=0)[0]
    thresh = 0.2
    y_pred = [[idx, res] for idx, res in enumerate(result) if res > thresh]

    y_pred.sort(key=lambda x: x[1], reverse=True)

    return_list = []
    for r in y_pred:
        return_list.append(r[0])
    return return_list
