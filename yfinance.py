import json
import os
import requests
from bs4 import BeautifulSoup

# ——— CONFIG ———
API_KEY           = "AIzaSyACQN8Po-5dHfsc3zZNR0nGH_tx66B1TiQ"  # your Google API key
CX_ID             = "5634a00ef882e4378"                      # your custom search engine ID
QUERIES           = ["rivian news"]                         # list of search queries
RESULTS_PER_QUERY = 10

SEEN_LINKS_FILE   = "seen_links.json"
PAGE_CONTENT_FILE = "page_content.json"


# ——— UTILITIES ———
def load_links(path):
    """Load a JSON list of seen URLs; return a set."""
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            pass
    return set()


def save_links(path, links):
    """Save a sorted list of URLs to JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sorted(links), f, indent=2, ensure_ascii=False)


def google_search(query):
    """
    Perform a Google Custom Search for `query`.
    Returns a set of result URLs.
    """
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q":    query,
        "key":  API_KEY,
        "cx":   CX_ID,
        "num":  RESULTS_PER_QUERY
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    items = resp.json().get("items", [])
    return {item["link"] for item in items}


def extract_text(html):
    """
    Given raw HTML, parse and return the concatenated
    text from <article> (if present) or all <p> tags.
    """
    soup = BeautifulSoup(html, "html.parser")
    container = soup.find("article") or soup
    paras = container.find_all("p")
    texts = [p.get_text(strip=True) for p in paras if p.get_text(strip=True)]
    return "\n\n".join(texts)


# ——— MAIN TASK ———
def scrape_all_articles():
    seen = load_links(SEEN_LINKS_FILE)
    page_map = {}

    # 1) Gather all search-result URLs
    all_results = set()
    for q in QUERIES:
        print(f"Searching for: {q!r}")
        all_results |= google_search(q)
    print(f"→ Found {len(all_results)} total result URLs\n")

    # 2) Fetch each unseen URL
    for url in sorted(all_results):
        if url in seen:
            continue

        try:
            print(f"Fetching: {url}")
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            html = r.text

            # 3) Extract the article text
            clean_text = extract_text(html)
            page_map[url] = {"text": clean_text}

            # 4) Mark URL as seen
            seen.add(url)
            print(f"  ✓ Extracted {len(clean_text)} chars of text\n")

        except Exception as e:
            print(f"  :warning: Error fetching {url}: {e}\n")

    # 5) Persist results
    save_links(SEEN_LINKS_FILE, seen)
    with open(PAGE_CONTENT_FILE, "w", encoding="utf-8") as f:
        json.dump(page_map, f, indent=2, ensure_ascii=False)

    print("Done! :arrow_forward:  Updated seen_links.json and page_content.json")


if __name__ == "__main__":
    scrape_all_articles()