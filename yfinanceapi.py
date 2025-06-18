import yfinance as yf
import requests as rq

def pull_links(keyword, max_results, news_count):
    search_obj = yf.Search(keyword, max_results=100, news_count=100, enable_fuzzy_query=False) #change ticker
    recent_threshold = 86400 * 7 #7 days
    news_articles = search_obj.news

    import datetime as dt

    now_local = dt.datetime.now()
    seconds_since_epoch_local = now_local.timestamp()

    recent_articles_link = []
    for i in news_articles:
        if i["providerPublishTime"] > seconds_since_epoch_local - recent_threshold:
            recent_articles_link.append(i["link"])

    return recent_articles_link

def pull_source_data(url):
    response = rq.get(url)
    content = response.content
    return content


most_recent_article = pull_links("MSFT", 100, 100)[0]
print(most_recent_article)

data = pull_source_data(most_recent_article)
print(data)




