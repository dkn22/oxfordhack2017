import pandas as pd
import requests
import json


def make_news_requ(input_dict):
    base = 'https://newsapi.org/v2/'
    tree = input_dict['tree'] + "?"
    ###############

    date = 'from=' + input_dict['date']
    to = "to=" + input_dict['to']
    sortBy = 'sortBy=popularity'
    
    if not isinstance(input_dict['keywords'], str):
        keywords = "q=" + ',+'.join(input_dict['keywords'])
    else:
        keywords = "q=" + input_dict['keywords']

    if not isinstance(input_dict['sources'], str):
        sources = "sources=" + ','.join(input_dict['sources'])
    else:
        sources = "sources=" + input_dict['sources']

    api_key = "apiKey=bbc19a8158e147b79f964c7155272cb4"

    add_on = ""

    for dic, ins in [["sources", sources], ["sortBy", sortBy], ["date", date], ['to', to]]:
        if len(input_dict[dic]) != 0:
            # print(input_dict[dic])
            add_on += "&" + ins

    url = base + tree + keywords + add_on + "&" + api_key

    response = requests.get(url)
    jsonified = json.loads(response.text)

    atr = jsonified['articles']
    df = pd.DataFrame(columns=atr[0].keys())

    for x in atr[1:]:
        x['source'] = x['source']['name']
        df = df.append(x, ignore_index=True)

    return df
