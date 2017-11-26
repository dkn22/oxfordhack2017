import sys
import os
import urllib.request, urllib.parse, urllib.error
from textblob import TextBlob
from nltk.tokenize import RegexpTokenizer
import numpy as np
import http
import json
from keras.preprocessing import sequence
from keras.models import model_from_json
sys.path.append(os.getcwd())
import models.cnn


# Make political slant analysis based on self trained CNN.
# @param[in]    df      articles data frame containing text.
def slant_analysis(df, vocab, model_filename):
    with open('/Users/Sele/Desktop/oxfordhack2017/models/vocab.json', 'r') as f:
        data = json.loads(f.read())
    WORD2IDX = data
    #model, graph = models.cnn.load(model_filename=model_filename)
    assert df.isnull().sum() == 0
    test_idxs = [np.array(word_to_idx(t, WORD2IDX)) for t in df['text'] if isinstance(t, str)]
    x_test = np.array(test_idxs)
    x_test = sequence.pad_sequences(x_test, maxlen=1000, value=0)
    with open('models/model.json', 'r') as f:
        model = model_from_json(f.read())
    model.load_weights('models/weights.best.hdf5')
    model.predict(x_test)
    df['slant'] = model.predict(x_test)#df['text'].apply(func=slant_single, args=(model, graph, vocab))
    return df

# Make text bias analysis built on data frame.
# @param[in]    df      articles data frame containing text.
def text_bias_analysis(df):
    df['text_bias'] = df['text'].apply(func=text_bias_single)
    return df

# Make image bias analysis built on data frame.
# @param[in]    df                  articles data frame containing text.
# @param[in]    microsoft_api_key   Microsoft Image API Key.
def image_bias_analysis(df, microsoft_api_key, attributes, max_attributes):
    df['e_at_pic'] = df['urlToImage'].apply(func=emotion_to_image, args=microsoft_api_key)
    return df

# Evaluate URL by getting quotes out of article text and search bing for these.
# @param[in]    df                  articles data frame containing text.
# @param[in]:   microsoft_api_key   Microsoft Bing Search API_KEY.
def quote_check(df, microsoft_api_key):
    df['quotes_eval'] = df.apply(lambda x: quote_check_single(x['quotes'], microsoft_api_key), axis=1)
    return df

# Analyse slant of single text.
# @param[in]    text        text to analyse.
# @param[in]    model       classification model.
# @param[in]    graph       classification graph.
def slant_single(text, model, graph, vocab):
    doc = word_to_idx(document=text, vocab_dict=vocab)
    print(doc)
    return

# Analyse single text bias using TextBlob.
# @param[in]    text                text to analyse.
def text_bias_single(text):
    text_blob = TextBlob(text)
    return text_blob.sentiment

# Quotes check for single article.
# @param[in]    quotes              list of quotes in article.
# @param[in]:   microsoft_api_key   Microsoft Bing Search API_KEY.
def quote_check_single(quotes, microsoft_api_key):
    host = "api.cognitive.microsoft.com"
    path = "/bing/v7.0/search"
    headers = {'Ocp-Apim-Subscription-Key': microsoft_api_key}
    conn = http.client.HTTPSConnection(host)
    quotes_eval = []
    for quote in quotes:
        bing_query = urllib.parse.quote(string=quote)
        conn.request("GET", path + "?q=" + bing_query, headers=headers)
        response = conn.getresponse()
        response_jason = json.loads(response.read().decode("utf8"))
        try:
            response_jason['webPages']['totalEstimatedMatches']
            quotes_eval.append(True)
        except KeyError:
            quotes_eval.append(False)
    return quotes_eval


def key_with_max_val(dict):
    v = list(dict.values())
    k = list(dict.keys())
    return k[v.index(max(v))]


def word_to_idx(document, vocab_dict):
    tokenizer = RegexpTokenizer(r'\w+')
    document = tokenizer.tokenize(document)
    seq_len = 1000
    x_train = [vocab_dict[word] for word in document if word in vocab_dict.keys()]
    return sequence.pad_sequences(np.array(x_train), maxlen=seq_len, value=0)


def emotion_to_image(url, microsoft_api_key):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': microsoft_api_key,
    }
    params = urllib.parse.urlencode({})
    body = {"url": url}
    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/emotion/v1.0/recognize?", str(body), headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        data = json.loads(data)
        return key_with_max_val(data[0]['scores'])
    except:
        return []