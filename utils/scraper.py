import feedparser
import json
from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup

RSS_FEED_URL = "https://www.cnbc.com/id/100003114/device/rss/rss.html"  # CNBC Top News
HEADERS = {
    'User-Agent': 'Mozilla/5.0',
    'Accept-Language': 'en-US,en;q=0.9',
}

def fetch_rss_news():
    feed = feedparser.parse(RSS_FEED_URL)

    articles = []
    for entry in feed.entries[:10]:
        title = entry.title
        link = entry.link

        try:
            article_resp = requests.get(link, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(article_resp.text, "html.parser")
            paragraphs = soup.select("div.ArticleBody-articleBody p")
            content = " ".join(p.text.strip() for p in paragraphs)

            if len(content.strip()) < 100:
                continue

            articles.append({
                "title": title,
                "url": link,
                "content": content,
                "timestamp": datetime.utcnow().isoformat()
            })
        except Exception as e:
            print(f"Skipping {title} due to error: {e}")
            continue

    os.makedirs("data", exist_ok=True)
    with open("data/news_raw.json", "w") as f:
        json.dump(articles, f, indent=2)

    print(f"Fetched {len(articles)} articles from CNBC RSS")

if __name__ == "__main__":
    fetch_rss_news()
