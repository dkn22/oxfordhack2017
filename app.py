from flask import Flask, render_template, request, jsonify
import datetime
import numpy as np
import json

import core.news
import core.newshandler
from models import cnn

# API Keys.
MICROSOFT_BING_API_KEY = 'cca69e754980473f81b0261ea2dde063'
MICROSOFT_VISION_API_KEY = '4b5604997f8747448756700dfac8a51d'
NEWS_API_KEY = 'c4dedaa7514f458d9f2700b76a678930'
# Analysis constants.
IMAGE_ATTRIBUTES = ['age', 'glasses', 'smile', 'gender']
IMAGE_MAX_ATTRIBUTES = ['emotion', 'facialHair']

with open('models/vocab.json', 'r') as f:
    data = json.loads(f.read())
WORD2IDX = data

app = Flask(__name__)

example_api = "http://[hostname]/todo/api/scores/?keyword=Trump&datefrom=20171117&date=20171118&sources=bbc-news"

@app.route('/todo/api/scores/',
           methods=['GET'],
           defaults={'keyword': None,
                     'datefrom': None,
                     'dateto': None,
                     'country': None,
                     'sources': None})
def produce_entity(keyword,
                   datefrom,
                   dateto,
                   country,
                   sources):
    # Get user input from web interface.
    keyword = request.args.get('keyword')
    date_from = request.args.get('datefrom')
    date_to = request.args.get('dateto')
    sources = request.args.get('sources')
    country = request.args.get('country')
    input_data = {'keywords': str(keyword).replace('%20', ' '),
                  'date': '' if not date_from else date_from,
                  'to': datetime.datetime.now().isoformat() if not date_to else date_to,
                  'sources': [] if not sources else sources,
                  'country': [] if not country else country,
                  'tree': 'everything',
                  'sortBy': 'popularity'}
    df = core.newshandler.newsletter_data_frame(
        input_dict=input_data, news_api_key=NEWS_API_KEY)
    # Text bias analysis.
    df = core.news.text_bias_analysis(df=df)
    # Image bias analysis.
    df = core.news.image_bias_analysis(df=df, microsoft_api_key=MICROSOFT_VISION_API_KEY,
                                       attributes=IMAGE_ATTRIBUTES, max_attributes=IMAGE_MAX_ATTRIBUTES)
    # Quotations analysis.
    df = core.news.quote_check(df=df, microsoft_api_key=MICROSOFT_BING_API_KEY)
    # Political slant analysis.
    df = core.news.slant_analysis(df=df, vocab=WORD2IDX, model_filename='models/model.json')
    # Return resulting data frame.
    articles_json = df.to_json(orient='records')
    return articles_json


if __name__ == '__main__':
    app.run(debug=True)