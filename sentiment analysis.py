import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd
import link_grabber 
from link_grabber import get_rss_links
from bs4 import BeautifulSoup
import requests

# nltk.download('all') 
#only run once

links = []

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    processed_text = ' '.join(lemmatized_tokens)
    return processed_text

analyzer = SentimentIntensityAnalyzer()
def get_sentiment(text):
    text = preprocess_text(text)
    scores = analyzer.polarity_scores(text)
    return scores['compound']

yahoo_finance_url = "https://finance.yahoo.com/news/rssindex"
cnbc_url = "https://www.cnbc.com/id/100003114/device/rss/rss.html"

# --- Get and display links from Yahoo Finance ---
print(f"--- Links from Yahoo Finance ({yahoo_finance_url}) ---")
yahoo_links = get_rss_links(yahoo_finance_url)

if yahoo_links:
    for i, link in enumerate(yahoo_links):
        links.append(link)
else:
    print("Could not retrieve links from Yahoo Finance. (Check for access restrictions or the URL).")

print("\n" + "="*70 + "\n") # Separator for clarity

# --- Get and display links from CNBC ---
print(f"--- Links from CNBC ({cnbc_url}) ---")
cnbc_links = get_rss_links(cnbc_url)

if cnbc_links:
    for i, link in enumerate(cnbc_links):
        links.append(link)
else:
    print("Could not retrieve links from CNBC. (Check for access restrictions or the URL).")

def extract_text(html):
    """
    Given raw HTML, parse and return the concatenated
    text from <article> (if present) or all <p> tags.
    """
    soup = BeautifulSoup(html, "html.parser")
    container = soup.find("article") or soup
    paras = container.find_all("p")
    texts = [p.get_text(strip=True) for p in paras if p.get_text(strip=True)]
    print(texts[:1])
    return "\n\n".join(texts)

for link in links:
    try:
        response = requests.get(link, timeout=10)
        response.raise_for_status()
        for i in range(100):
            pass
        html = response.text

        article_text = extract_text(html)
        print(article_text)

        sentiment_score = get_sentiment(article_text)
        print(f"Link: {link}\nSentiment Score: {sentiment_score}\n")
    except Exception as e:
        print(f"Error processing {link}: {e}")