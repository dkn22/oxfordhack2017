import pandas as pd
import requests
import json
import newspaper

# Getting news article data frame using NewsAPI.
# @param[in]:   input_dict      input query containing q, tree, keywords,
#                               date, sources and sortBy.
# @param[in]:   news_api_key    NewsAPI_KEY.
def newsletter_data_frame(input_dict, news_api_key):
    # Parse input arguments from input dictionary.
    base = 'https://newsapi.org/v2/'
    tree = input_dict['tree'] + "?"
    date = 'from=' + input_dict['date']
    to = "to=" + input_dict['to']
    sort_by = 'sortBy=popularity'
    if not isinstance(input_dict['keywords'], str):
        keywords = "q=" + ',+'.join(input_dict['keywords'])
    else:
        keywords = "q=" + input_dict['keywords']
    if not isinstance(input_dict['sources'], str):
        sources = "sources=" + ','.join(input_dict['sources'])
    else:
        sources = "sources=" + input_dict['sources']
    api_key = "apiKey=" + news_api_key
    add_on = ""
    for dic, ins in [["sources", sources], ["sortBy", sort_by], ["date", date], ['to', to]]:
        if len(input_dict[dic]) != 0:
            # print(input_dict[dic])
            add_on += "&" + ins
    url = base + tree + keywords + add_on + "&" + api_key
    # Get response given requested URL, jasonify and create data frame out of received data.
    response = requests.get(url)
    json_response = json.loads(response.text)
    atr = json_response['articles']
    df = pd.DataFrame(columns=atr[0].keys())
    # Add easy source access.
    for x in atr[1:]:
        x['source'] = x['source']['name']
        x['text'] = article_text(x['url'])
        df = df.append(x, ignore_index=True)
    return df


# Get text of single article using newspaper package.
# @param[in]    article_url     URL of article to analyse.
def article_text(article_url):
    try:
        article = newspaper.Article(url=article_url, language='en')
        article.download()
        article.parse()
        return article.text
    except newspaper.ArticleException:
        print("URL: %s not found" % article_url)
    return ""

