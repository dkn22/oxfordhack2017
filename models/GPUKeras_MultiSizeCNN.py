
# coding: utf-8

# In[1]:

from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Conv1D, Embedding, Concatenate, Input, MaxPooling1D, Flatten, SpatialDropout1D, Dropout
from keras.optimizers import Adam, SGD
from keras.preprocessing import image, sequence

from gensim.models.keyedvectors import KeyedVectors
from nltk.tokenize import RegexpTokenizer
import numpy as np
import json
import pandas as pd


# In[2]:

from tensorflow.python.client import device_lib

device_lib.list_local_devices()


# In[3]:

embeddings = KeyedVectors.load('word_embeddings')


# In[4]:

embeddings


# In[35]:

vocab = dict([(k, v.index) for k, v in embeddings.vocab.items()])
vocab_path = 'vocab.json'
with open(vocab_path, 'w') as f:
    f.write(json.dumps(vocab))


# In[6]:

idx2word = dict([(v, k) for k, v in embeddings.vocab.items()])


# In[12]:

weights = embeddings.syn0


# In[16]:

embedding_layer = Embedding(input_dim=weights.shape[0], output_dim=weights.shape[1], weights=[weights])


# # Preprocess data 

# In[14]:

speeches = pd.read_csv('CongressionalSpeeches.csv',
                      usecols=['speech', 'party'])


# In[15]:

tokens = []
tokenizer = RegexpTokenizer(r'\w+')
for i, s in enumerate(speeches['speech']):
    tokens.append(tokenizer.tokenize(s))
    
    if i % 10000 == 0:
        # print(i)


# In[17]:

n_fact = embedding_layer.get_config()['output_dim']
idx_tokens = [[vocab[word]
               for word in doc if word in vocab.keys()] \
               for doc in tokens]


# In[21]:

from sklearn.cross_validation import train_test_split

train_idxs, test_idxs, y_train, y_test = train_test_split(speeches.index, 
                                                          np.where(speeches['party'] == 'R', 1, 0),
                                                          test_size=0.2)


# In[22]:

x_train = np.array(idx_tokens)[train_idxs]
x_test = np.array(idx_tokens)[test_idxs]


# In[23]:

seq_len = 1000

trn = sequence.pad_sequences(x_train, maxlen=seq_len, value=0)
test = sequence.pad_sequences(x_test, maxlen=seq_len, value=0)


# In[24]:

trn.shape


# In[25]:

################# KERAS MODEL
vocab_size = len(vocab)

graph_in = Input((vocab_size, 100))
convs = [ ] 
for fsz in range (3, 6): 
    x = Conv1D(64, fsz, padding='same', activation="relu")(graph_in)
    x = MaxPooling1D()(x) 
    x = Flatten()(x) 
    convs.append(x)
out = Concatenate(axis=-1)(convs) 
graph = Model(graph_in, out)


# In[27]:

embedding_layer.input_length = seq_len


# In[28]:

model = Sequential([
    embedding_layer,
    SpatialDropout1D(0.2),
    Dropout (0.2),
    graph,
    Dropout (0.5),
    Dense (100, activation="relu"),
    Dropout (0.7),
    Dense (1, activation='sigmoid')
    ])


# In[29]:

model.compile(loss='binary_crossentropy', optimizer=Adam(), metrics=['accuracy'])


# In[ ]:

model.fit(trn, y_train, validation_data=(test, y_test), epochs=1, batch_size=64,
         verbose=1)


# In[ ]:

from keras.callbacks import ModelCheckpoint
filepath="weights.best.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]

model.fit(trn, y_train, validation_data=(test, y_test), epochs=5, batch_size=64,
         callbacks=callbacks_list,
         verbose=1)


# In[32]:

model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)


# In[33]:

from IPython.display import FileLink

FileLink('model.json')


# In[34]:

from IPython.display import FileLink

FileLink('weights.best.hdf5')


# In[36]:

from IPython.display import FileLink

FileLink('vocab.json')


# In[ ]:



