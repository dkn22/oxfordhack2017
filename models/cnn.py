import numpy as np
import keras.models
from keras.models import model_from_json

import tensorflow as tf

# Load CNN model from json file.
# @param[in]    model_filename  path to model file.
def load(model_filename):
    json_file = open(file=model_filename, mode='r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("weights.best.hdf5")
    loaded_model.compile(loss='binary_crossentropy',
                         optimizer='adam', metrics=['accuracy'])
    graph = tf.get_default_graph()
    return loaded_model, graph
