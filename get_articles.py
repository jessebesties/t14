import requests
from newspaper import Article
import time
from typing import List  # Python 3.7 fix

# --- Lista de todos los enlaces proporcionados ---
ALL_ARTICLE_URLS = [
    # (all your Yahoo Finance and CNBC URLs unchanged)
    "https://finance.yahoo.com/news/live/stock-market-today-dow-sp-500-nasdaq-rise-as-fed-takes-front-seat-from-mideast-fears-231755274.html",
    "https://finance.yahoo.com/news/corn-getting-spillover-support-wheat-172158799.html",
    "https://finance.yahoo.com/news/archer-aviation-betting-big-fledgling-171303847.html",
    "https://www.investors.com/news/economy/federal-reserve-meeting-june-rate-cut-outlook-jobless-claims-powell-sp-500/?src=A00220&yptr=yahoo",
    "https://finance.yahoo.com/news/prediction-losing-more-1-trillion-170800338.html",
    # ... continue your full list
    "https://www.cnbc.com/2025/06/17/genius-stablecoin-bill-crypto.html",
]

def extract_article_content_simple(urls: List[str]):
    """
    Extrae el título y el contenido principal de una lista de URLs
    usando newspaper3k.
    """
    extracted_articles = []
    print(f"Comenzando la extracción de contenido de {len(urls)} URLs...")

    for i, url in enumerate(urls):
        print(f"[{i+1}/{len(urls)}] Procesando: {url}")
        try:
            article = Article(url)
            article.download()
            article.parse()

            title = article.title or "Título no encontrado"
            content = article.text or "Contenido no encontrado"
            source_domain = url.split("//")[-1].split("/")[0]

            extracted_articles.append({
                "url": url,
                "title": title,
                "content": content,
                "source_domain": source_domain
            })

        except Exception as e:
            print(f"ERROR al procesar {url}: {e}")
        
        time.sleep(1)
    
    return extracted_articles

# --- Ejecutar la extracción ---
articles_data = extract_article_content_simple(ALL_ARTICLE_URLS)

# --- Mostrar los resultados ---
print("\n--- Extracción finalizada ---")
print(f"Se extrajo contenido de {len(articles_data)} artículos (ignorando errores).")

print("\n--- Primeros 5 artículos extraídos: ---")
for i, article in enumerate(articles_data[:5]):
    print(f"\nArtículo {i+1}:")
    print(f"  URL: {article['url']}")
    print(f"  Dominio: {article['source_domain']}")
    print(f"  Título: {article['title']}")
    print(f"  Contenido (primeros 200 caracteres): {article['content'][:200]}...")
    print("-" * 30)

import json
with open("extracted_articles_simple.json", "w", encoding="utf-8") as f:
    json.dump(articles_data, f, ensure_ascii=False, indent=4)
    print("\nTodos los artículos guardados en 'extracted_articles_simple.json'")
