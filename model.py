import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.regularizers import l2


def build_model(input_shape, output_shape):
    model = Sequential()
    model.add(Dense(128, input_shape=input_shape,
              activation="relu", kernel_regularizer=l2(1e-4)))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))
    model.add(Dense(64, activation="relu", kernel_regularizer=l2(1e-4)))
    model.add(BatchNormalization())
    model.add(Dropout(0.3))
    model.add(Dense(output_shape, activation="softmax"))

    adam = tf.keras.optimizers.Adam(learning_rate=0.01, weight_decay=1e-6)
    model.compile(loss='categorical_crossentropy',
                  optimizer=adam, metrics=["accuracy"])
    return model


def train_model(model, train_X, train_y, epochs=200):
    model.fit(x=train_X, y=train_y, epochs=epochs, verbose=1)
    return model
