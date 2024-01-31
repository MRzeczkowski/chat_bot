import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense, BatchNormalization, Dropout
from tensorflow.keras.regularizers import l2


def build_model(word_index, output_dim):
    embed_dim = 300
    lstm_num = 50

    model = Sequential([
        Embedding(len(word_index) + 1, embed_dim),
        Bidirectional(
            LSTM(lstm_num, dropout=0.4)),
        Dense(lstm_num, activation='relu',
              kernel_regularizer=l2(1e-4)),
        BatchNormalization(),
        Dropout(0.5),
        Dense(output_dim, activation='softmax')
    ])

    optimizer = tf.keras.optimizers.Adam(
        learning_rate=0.001, weight_decay=1e-6)

    model.compile(optimizer=optimizer,
                  loss='categorical_crossentropy', metrics=['accuracy'])

    return model


def train_model(model, padded_sequences, categorical_vec, epochs=100):
    model.fit(padded_sequences, categorical_vec, epochs=epochs, verbose=0)
    return model
