from flask import Flask, render_template, request, jsonify
import re

import pandas as pd
import requests
import json

import datetime

from news import make_news_requ

app = Flask(__name__)

example_api = "http://[hostname]/todo/api/scores/?keyword=Trump&datefrom=20171117&date=2017118&sources=bbc-news"


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

    keyword = request.args.get('keyword')
    datefrom = request.args.get('datefrom')
    dateto = request.args.get('dateto')
    sources = request.args.get('sources')
    country = request.args.get('country')

    input_data = {'keywords': str(keyword).replace('%20', ' '),
                  'date': '' if not datefrom else datefrom,
                  'to': datetime.datetime.now().isoformat() if not dateto else dateto,
                  'sources': [] if not sources else sources,
                  'country': [] if not country else country,
                  'tree': 'everything',
                  'sortBy': 'popularity'}
    df = make_news_requ(input_data)

    jsonified_articles = df.to_json(orient='records')
    return jsonified_articles


if __name__ == '__main__':
    app.run(debug=True)
