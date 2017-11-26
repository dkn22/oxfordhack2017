
# coding: utf-8

# In[22]:

import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import CountVectorizer


# In[2]:

speeches = pd.read_csv('CongressionalSpeeches.csv')


# In[13]:

speeches['speech_length'] = speeches['speech'].apply(len)


# In[ ]:

# speeches_ = speeches[(speeches.speech_length > 100) & (speeches.speech_length < 1000)]


# In[24]:

speeches['target'] = np.where(speeches['party'] == 'R', 1, 0)

speeches['target'].head()


# In[3]:

vectorizer = CountVectorizer(stopwords='english')

vectorizer.fit(speeches['speech'])


# In[5]:

bow = vectorizer.transform(speeches['speech'])


# In[10]:

from sklearn.model_selection import train_test_split


# In[8]:

from sklearn.linear_model import LogisticRegressionCV


# In[25]:

train_X, test_X, train_y, test_y = train_test_split(bow, speeches['target'], test_size=0.2)


# In[27]:

model = LogisticRegressionCV(Cs=[1e-3, 1e-2, 1e-1, 1, 1e10, 1e100], n_jobs=-1)

model.fit(train_X, train_y)


# In[28]:

from sklearn.metrics import accuracy_score


# In[29]:

accuracy_score(model.predict(test_X), test_y)


# In[30]:

accuracy_score(model.predict(train_X), train_y)


# In[32]:

joblib.dump(model, 'logistic_classifier.pkl')


# In[ ]:



