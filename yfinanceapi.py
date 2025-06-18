import yfinance as yf
import requests as rq

search_obj = yf.Search("MSFT", max_results=100, news_count=100) #change ticker
recent_threshold = 86400 * 7 #7 days
news_articles = search_obj.news

import datetime as dt

now_local = dt.datetime.now()
seconds_since_epoch_local = now_local.timestamp()

recent_articles = []
for i in news_articles:
    if i["providerPublishTime"] > seconds_since_epoch_local - recent_threshold:
        recent_articles.append(i)

for i in recent_articles:
    print(i)

