import requests
import urllib.request, urllib.parse, urllib.error
import io
from textblob import TextBlob

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
    with urllib.request.urlopen(image_url) as url:
        img_data = io.BytesIO(url.read())
    try:
        response = requests.post(uri_base + path_to_face_api,
                                 data=img_data,
                                 headers=headers,
                                 params=params)
        parsed = response.json()
    except Exception as e:
        parsed = []
    # Check response for feature.
    if len(parsed) == 0:
        return "no faces"
    # Analyse received results under given attributes.
    else:
        facial_tempdic = {}
        for att in attributes:
            facial_tempdic[att] = parsed[0]['faceAttributes'][att]
        for att in max_attributes:
            stats = parsed[0]['faceAttributes'][att]
            facial_tempdic[att] = key_with_max_val(stats) + " " + str(stats[key_with_max_val(stats)])
        return facial_tempdic


def key_with_max_val(d):
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]


