import numpy as np
import keras.models
from keras.models import model_from_json

import tensorflow as tf


def load():

    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load woeights into new model
    loaded_model.load_weights("weights.best.hdf5")

    loaded_model.compile(loss='binary_crossentropy',
                         optimizer='adam', metrics=['accuracy'])

    graph = tf.get_default_graph()

    return loaded_model, graph
