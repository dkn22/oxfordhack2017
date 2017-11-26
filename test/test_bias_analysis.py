import sys
import os
import json
sys.path.append(os.getcwd())

import core.newshandler
import core.news

with open('/Users/Sele/Desktop/oxfordhack2017/models/vocab.json', 'r') as f:
    data = json.loads(f.read())
WORD2IDX = data

# API Keys.
MICROSOFT_BING_API_KEY = 'cca69e754980473f81b0261ea2dde063'
MICROSOFT_VISION_API_KEY = '4b5604997f8747448756700dfac8a51d'
NEWS_API_KEY = 'c4dedaa7514f458d9f2700b76a678930'
# Analysis constants.
IMAGE_ATTRIBUTES = ['age', 'glasses', 'smile', 'gender']
IMAGE_MAX_ATTRIBUTES = ['emotion', 'facialHair']
# Example input data dictionary.
input_data = {'keywords': "Trump",
              'date': '' "20171117",
              'to': "20171118",
              'sources': [],
              'country': [],
              'tree': 'everything',
              'sortBy': 'popularity'}

if __name__ == '__main__':
    df = core.newshandler.newsletter_data_frame(input_dict=input_data, news_api_key=NEWS_API_KEY)
    # Text bias analysis.
    #df = core.news.text_bias_analysis(df=df)
    # Image bias analysis.
    #df = core.news.image_bias_analysis(df=df, microsoft_api_key=MICROSOFT_VISION_API_KEY, \
    #                                   attributes=IMAGE_ATTRIBUTES, max_attributes=IMAGE_MAX_ATTRIBUTES)
    # Quote analysis.
    #df = core.news.quote_check(df=df, microsoft_api_key=MICROSOFT_BING_API_KEY)
    # Slant analysis.
    df = core.news.slant_analysis(df=df, vocab=WORD2IDX, model_filename='/Users/Sele/Desktop/oxfordhack2017/models/model.json')
    print(df)
