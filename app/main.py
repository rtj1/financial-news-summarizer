from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import threading
import time
import subprocess
import gradio as gr
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()
app.add_middleware(GZipMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = "data/news_ranked.json"

# === Background Refresh Thread ===
def auto_refresh():
    while True:
        try:
            subprocess.run(["python", "utils/scraper.py"], check=True)
            subprocess.run(["python", "model/summarizer.py"], check=True)
            subprocess.run(["python", "utils/ranker.py"], check=True)
            print("Data refreshed.")
        except Exception as e:
            print(f"Refresh failed: {e}")
        time.sleep(600)  # every 10 mins

@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=auto_refresh, daemon=True)
    thread.start()

# === API Endpoint ===
@app.get("/news")
def get_news():
    if not os.path.exists(DATA_PATH):
        return JSONResponse(content={"message": "No data available"}, status_code=404)
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    return {"news": data}

# === Gradio UI Mounted at /dashboard ===
def build_gradio_app():
    def load_articles():
        if not os.path.exists(DATA_PATH):
            return []
        with open(DATA_PATH, "r") as f:
            return json.load(f)

    def get_choices():
        articles = load_articles()
        return [f"{i+1}. {a['title'][:80]}" for i, a in enumerate(articles)]

    def show_article(choice_text):
        articles = load_articles()
        try:
            index = int(choice_text.split(".")[0]) - 1
            a = articles[index]
            return f"""### {a['title']}

**Summary**  
{a['summary']}

**Sentiment:** `{round(a['sentiment_score'], 2)}`  
**Relevance:** `{round(a['relevance_score'], 2)}`  
[Read full article]({a['url']})
"""
        except:
            return "⚠️ Could not load article."

    def refresh_data():
        try:
            subprocess.run(["python", "utils/scraper.py"], check=True)
            subprocess.run(["python", "model/summarizer.py"], check=True)
            subprocess.run(["python", "utils/ranker.py"], check=True)
        except Exception as e:
            return f"❌ Error: {e}"
        return "✅ News updated!"

    with gr.Blocks() as demo:
        gr.Markdown("# 🧠 Real-Time Financial News Summarizer")
        with gr.Row():
            refresh_btn = gr.Button("🔄 Refresh News")
            status_box = gr.Textbox(label="Status", value="")

        news_radio = gr.Radio(choices=get_choices(), label="Select a news article")
        output_box = gr.Markdown()

        refresh_btn.click(fn=refresh_data, outputs=status_box).then(fn=get_choices, outputs=news_radio)
        news_radio.change(fn=show_article, inputs=news_radio, outputs=output_box)

    return demo

# Mount Gradio to /dashboard
app = gr.mount_gradio_app(app, build_gradio_app(), path="/dashboard")

# Optional: Redirect root to dashboard
@app.get("/")
def redirect_to_dashboard():
    return RedirectResponse("/dashboard")
