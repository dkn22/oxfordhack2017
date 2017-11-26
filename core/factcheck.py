# APIS: LUIS, Microsoft Text Recognition, Microsoft Bing Search, NewsAPI, StrepHit, TextBlobb

import requests
import json
import newspaper
from multiprocessing import Pool
import nltk
import http.client
import urllib.parse
import matplotlib.pyplot as plt

#nltk.download('averaged_perceptron_tagger')
#nltk.download('maxent_ne_chunker')
#nltk.download('words')

MICROSOFT_API_KEY = 'cca69e754980473f81b0261ea2dde063'
NEWS_API_KEY = 'c4dedaa7514f458d9f2700b76a678930'
INPUT_DICT = {'tree': "everything", "sources": [], 'sortBy': 'popularity', 'keywords': ['trump'],"date": ""}

# Get json from NewsAPI.
# @param[in]:   input_dict      input query containing q, tree, keywords,
#                               date, sources and sortBy.
# @param[in]:   api_key         NewsAPI_KEY.
def news_json(input_dict, api_key):
    base = 'https://newsapi.org/v2/'
    tree = input_dict['tree'] + "?"
    keywords = "q=" + ',+'.join(input_dict['keywords'])
    date = 'from=' + input_dict['date']
    sort_by = 'sortBy=popularity'
    sources = "sources=" + ','.join(input_dict['sources'])
    api_key = "apiKey=" + api_key
    add_on = ""
    for dic, ins in [["sources", sources], ["sortBy", sort_by], ["date", date]]:
        if len(input_dict[dic]) != 0:
            print(input_dict[dic])
            add_on += "&" + ins
    # Parse query from given input.
    query = base + tree + keywords + add_on + "&" + api_key
    # Call Microsoft API to get according
    response = requests.get(query)
    jason = json.loads(response.text)
    return jason

# Get text of single article.
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

# Get newspaper articles text according to given query using NewsAPI.
# @param[in]:   input_dict      input query containing q, tree, keywords,
#                               date, sources and sortBy.
# @param[in]:   news_api_key    NewsAPI key.
def article_dict(input_dict, news_api_key):
    results = news_json(input_dict=input_dict, api_key=news_api_key)
    # Get dictionary with newspaper articles texts.
    urls = [result['url'] for result in results['articles']]
    # Download article and build dictionary multi_threaded.
    pool = Pool(len(urls))
    texts = pool.map(article_text, urls)
    if not len(texts) == len(urls):
        raise RuntimeError("article_dict(): Array sizes do not match !")
    url_text_dict = {}
    for x in range(0, len(texts)):
        url_text_dict[urls[x]] = texts[x]
    return url_text_dict

# Evaluate URL by getting entities out of article text and search bing for
# these entities. Return dictionary mapping URL to quote/sentence to evaluation.
# @param[in]    url_text_dict   dictionary mapping URLs to containing article text.
# @param[in]:   api_key         MicrosoftAPI_KEY.
def check_url_dictionary(url_text_dict, api_key):
    url_sentence_eval = {}
    for url, text in url_text_dict.items():
        queries = text_to_quotations(text)
        sentence_eval = {}
        for query in queries:
            bing_results = search_bing(query=query, api_key=api_key)
            try:
                bing_results['webPages']['totalEstimatedMatches']
                sentence_eval[query] = True
            except KeyError:
                sentence_eval[query] = False
        url_sentence_eval[url] = sentence_eval
    return url_sentence_eval

# Convert sentence to quotation entities list.
def text_to_quotations(text):
    quotation_sep = text.split('"')
    citations = []
    for i in range(0, len(quotation_sep)):
        if not i % 2 == 0:
            citations.append(quotation_sep[i])
        else:
            pass
    return citations


# Search for Bing results given an entity and return found results.
# @param[in]    query           query to Bing search.
# @param[in]:   api_key         MicrosoftAPI_KEY.
def search_bing(query, api_key):
    host = "api.cognitive.microsoft.com"
    path = "/bing/v7.0/search"
    headers = {'Ocp-Apim-Subscription-Key': api_key}
    conn = http.client.HTTPSConnection(host)
    bing_query = urllib.parse.quote(string=query)
    conn.request("GET", path + "?q=" + bing_query, headers=headers)
    response = conn.getresponse()
    return json.loads(response.read().decode("utf8"))


# Distribution of number of words in article.
# @param[in]    article_text_dict   map from article to full text.
def text_size_distribution(article_text_dict):
    num_words = []
    for article, text in article_text_dict.items():
        text_size = len(nltk.word_tokenize(text))
        num_words.append(text_size)
    plt.hist(num_words, 50)
    plt.show()


if __name__ == '__main__':
    article_text_dict = article_dict(input_dict=INPUT_DICT, news_api_key=NEWS_API_KEY)
    url_sentence_eval_dict = check_url_dictionary(url_text_dict=article_text_dict, api_key=MICROSOFT_API_KEY)
    print(url_sentence_eval_dict.keys())

