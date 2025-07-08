import json
from transformers import pipeline
import os

# Load summarizer pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_articles(input_path="data/news_raw.json", output_path="data/news_summaries.json"):
    if not os.path.exists(input_path):
        print(f"No input file found at {input_path}")
        return

    with open(input_path, "r") as f:
        articles = json.load(f)

    summarized_articles = []
    for article in articles:
        content = article.get("content", "")
        if len(content.strip().split()) < 10:
            print(f"Skipping short article: {article.get('title')}")
            continue

        try:
            summary = summarizer(content, max_length=130, min_length=30, do_sample=False)[0]["summary_text"]
        except Exception as e:
            print(f"Error summarizing article: {e}")
            continue

        summarized_articles.append({
            "title": article.get("title"),
            "url": article.get("url"),
            "summary": summary,
            "timestamp": article.get("timestamp")
        })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(summarized_articles, f, indent=2)

    print(f"Summarized {len(summarized_articles)} articles.")

if __name__ == "__main__":
    summarize_articles()
