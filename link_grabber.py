import feedparser
import requests # requests is used by feedparser internally for downloading

final_links = []

def get_rss_links(url):
    """
    Retrieves article links from an RSS feed.

    Args:
        url (str): The URL of the RSS feed.

    Returns:
        list: A list of strings, where each string is an article link.
              Returns an empty list if there's an error or no links are found.
    """
    try:
        # feedparser handles downloading and parsing automatically
        feed = feedparser.parse(url)

        # Basic error handling if the feed cannot be fetched or parsed
        if feed.bozo:
            if hasattr(feed, 'status') and feed.status != 200:
                print(f"Error fetching RSS feed (status code: {feed.status}) for {url}: {feed.bozo_exception}")
            else:
                print(f"Warning parsing feed (possible formatting errors) for {url}: {feed.bozo_exception}")
            return []

        links = []
        for entry in feed.entries:
            link = entry.get('link', None) # Get the link; if it doesn't exist, return None
            if link: # Only add the link if it exists
                links.append(link)
        return links
    except Exception as e:
        print(f"General error fetching or parsing RSS from {url}: {e}")
        return []

# --- RSS Feed URLs ---
yahoo_finance_url = "https://finance.yahoo.com/news/rssindex"
cnbc_url = "https://www.cnbc.com/id/100003114/device/rss/rss.html"

# --- Get and display links from Yahoo Finance ---
print(f"--- Links from Yahoo Finance ({yahoo_finance_url}) ---")
yahoo_links = get_rss_links(yahoo_finance_url)

if yahoo_links:
    for i, link in enumerate(yahoo_links):
        final_links.append(link)
else:
    print("Could not retrieve links from Yahoo Finance. (Check for access restrictions or the URL).")

print("\n" + "="*70 + "\n") # Separator for clarity

# --- Get and display links from CNBC ---
print(f"--- Links from CNBC ({cnbc_url}) ---")
cnbc_links = get_rss_links(cnbc_url)

if cnbc_links:
    for i, link in enumerate(cnbc_links):
        final_links.append(link)
else:
    print("Could not retrieve links from CNBC. (Check for access restrictions or the URL).")

