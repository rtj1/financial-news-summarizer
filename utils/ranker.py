import json
import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download("vader_lexicon")

PORTFOLIO_KEYWORDS = ["inflation", "interest rates", "GDP", "Federal Reserve", "earnings", "volatility", "merger", "acquisition", "regulation", "recession"]

def compute_scores(input_path="data/news_summaries.json", output_path="data/news_ranked.json"):
    if not os.path.exists(input_path):
        print(f"No input found at {input_path}")
        return

    with open(input_path, "r") as f:
        summaries = json.load(f)

    if len(summaries) < 2:
        print("Not enough articles for relevance scoring. Skipping ranking.")
        with open(output_path, "w") as f:
            json.dump(summaries, f, indent=2)
        return

    sid = SentimentIntensityAnalyzer()
    tfidf = TfidfVectorizer()

    texts = [article["summary"] for article in summaries]
    keyword_doc = [" ".join(PORTFOLIO_KEYWORDS)]
    matrix = tfidf.fit_transform(texts + keyword_doc)

    relevance_scores = cosine_similarity(matrix[:-1], matrix[-1])

    ranked_articles = []
    for i, article in enumerate(summaries):
        sentiment = sid.polarity_scores(article["summary"])["compound"]
        relevance = float(relevance_scores[i])
        article["sentiment_score"] = sentiment
        article["relevance_score"] = relevance
        article["total_score"] = sentiment + relevance
        ranked_articles.append(article)

    ranked_articles.sort(key=lambda x: x["total_score"], reverse=True)

    with open(output_path, "w") as f:
        json.dump(ranked_articles, f, indent=2)

    print(f"Ranked {len(ranked_articles)} articles.")

if __name__ == "__main__":
    compute_scores()
