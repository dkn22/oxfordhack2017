
# coding: utf-8

# In[21]:

import re

import pandas as pd
import numpy as np
from joblib import Parallel, delayed

import gensim
from nltk.tokenize import PunktSentenceTokenizer


# In[3]:

data = pd.read_csv('CongressionalSpeeches.csv')


# In[4]:

speeches = data['speech']


# In[5]:

speeches.head()


# In[14]:

tokenizer = PunktSentenceTokenizer()
abbreviations = ['dr', 'mr', 'ms', 'mrs', 'prof',
                'gov', 'sen', 'ny', 'la']
tokenizer._params.abbrev_types.add('dr')
tokenizer._params.abbrev_types.add('mr')
tokenizer._params.abbrev_types.add('ms')
tokenizer._params.abbrev_types.add('mrs')
tokenizer._params.abbrev_types.add('prof')


# In[24]:

sentences = list(Parallel(n_jobs=-1)(delayed(tokenizer.tokenize)(x) for x in speeches))


# In[32]:

word_lists = []

for s in sentences:
    
    words = [re.sub("[^\w]", " ",  sentence).split()                             for sentence in s]
    
    word_lists.append(words)


# In[39]:

model = gensim.models.Word2Vec(word_lists[0],min_count=0)


# In[48]:

with open('sentences.txt', 'w') as f:
    for doc_idx, sentence in enumerate(sentences):
        f.write('Document number %d \n' %doc_idx)
        for s in sentence:
            f.write(s+'\n')


# In[49]:

len(sentences)


# In[51]:

speeches.shape


# In[54]:

import itertools
all_sentences = itertools.chain.from_iterable(word_lists)


# In[55]:

word2vec = gensim.models.Word2Vec(all_sentences, min_count=50, size=100, workers=4)


# In[58]:

word2vec.save('word_embeddings.pkl')


# In[60]:

weights = word2vec.syn0


# In[74]:

word2vec.wv.save('word_embeddings')

