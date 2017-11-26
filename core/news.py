import sys
import os
import requests
import urllib.request, urllib.parse, urllib.error
import io
from textblob import TextBlob
from nltk.tokenize import RegexpTokenizer
import numpy as np

sys.path.append(os.getcwd())
import models.cnn

# Make political slant analysis based on self trained CNN.
# @param[in]    df              articles data frame containing text.
# @param[in]    vocab           vocabulary (words->numbers) dictionary.
# @param[in]    model_filename  path to model file.
def slant_analysis(df, vocab, model_filename):
    docs = []
    for article in df['text']:
        docs.append(word_to_idx(document=article, vocab_dict=vocab))
    model, graph = models.cnn.load(model_filename=model_filename)
    df['slant'] = df['text'].apply(func=slant_single, args=(model, graph))
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
    df['e_at_pic'] = df['urlToImage'].apply(func=image_bias_single, \
                                            args=(microsoft_api_key, attributes, max_attributes))
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
def slant_single(text, model, graph):
    with graph.as_default():
        prediction = model.predict(np.array(docs))
        classification = np.where(prediction >= 0.5, 'Right', 'Left')
    return {'prediction': prediction, 'classification': classification}

# Analyse single text bias using TextBlob.
# @param[in]    text                text to analyse.
def text_bias_single(text):
    text_blob = TextBlob(text)
    return text_blob.sentiment

# Analyse single image bias using Microsoft Vision API.
# @param[in]    image_url           URL to image to analyse.
# @param[in]    microsoft_api_key   Microsoft Image API Key.
def image_bias_single(image_url, microsoft_api_key, attributes, max_attributes):
    # Parse input arguments for Microsoft API Service.
    uri_base = 'https://westcentralus.api.cognitive.microsoft.com'
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': microsoft_api_key, }
    params = {
        'returnFaceId': 'true', 'Adult': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,smile,facialHair,glasses,emotion,hair,makeup'}
    path_to_face_api = '/face/v1.0/detect'
    # Get image classification and parse response.
    try:
        url = urllib.request.urlopen(image_url)
        img_data = io.BytesIO(url.read())
        response = requests.post(uri_base + path_to_face_api,
                                 data=img_data,
                                 headers=headers,
                                 params=params)
        parsed = response.json()
    except urllib.error.URLError:
        print("image_bias_single(): Could not open URL %s" % image_url)
        return "image_bias_single(): No faces received !"
    # Check response for feature.
    # Analyse received results under given attributes.
    try:
        facial_temp_dic = {}
        for att in attributes:
            facial_temp_dic[att] = parsed[0]['faceAttributes'][att]
        for att in max_attributes:
            stats = parsed[0]['faceAttributes'][att]
            facial_temp_dic[att] = key_with_max_val(stats) + " " + str(stats[key_with_max_val(stats)])
        return facial_temp_dic
    except KeyError:
        print("image_bias_single(): Bad parsed string")
        return "image_bias_single(): No faces received !"

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
    return [vocab_dict[word] for word in document if word in vocab_dict.keys()]