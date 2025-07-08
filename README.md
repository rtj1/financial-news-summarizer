# 🧠 Real-Time Financial News Summarizer

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/Gradio-Dashboard-orange?logo=gradio)](https://www.gradio.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is a real-time GenAI-powered dashboard that scrapes, summarizes, and ranks financial news headlines from CNBC using a fine-tuned LLM pipeline.

---

## 🔍 Features

- ✅ Scrapes CNBC RSS feed and extracts full article text
- ✅ Summarizes each article using `facebook/bart-large-cnn`
- ✅ Scores each item by:
  - Sentiment (via VADER)
  - Relevance to finance using TF-IDF
- ✅ Interactive Gradio Dashboard:
  - Refresh news
  - View summaries and scores
  - Click to open full articles

---

## 📦 Project Structure

```
financial-news-summarizer/
├── app/
│   ├── main.py               # FastAPI backend
│   └── gradio_dashboard.py   # Gradio frontend
├── model/
│   └── summarizer.py         # Summarization pipeline
├── utils/
│   ├── scraper.py            # CNBC RSS + full article scraping
│   └── ranker.py             # Sentiment + relevance ranking
├── data/                     # Auto-generated JSON storage
│   └── news_raw.json
├── requirements.txt
├── Dockerfile
└── start.sh
```

---

## 🚀 Quick Start

### 🔧 Local Setup
```bash
git clone https://github.com/YOUR_USERNAME/financial-news-summarizer.git
cd financial-news-summarizer
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### ▶ Run the Gradio Dashboard
```bash
python app/gradio_dashboard.py
```

### 🔁 Refresh News Manually (optional)
```bash
python utils/scraper.py
python model/summarizer.py
python utils/ranker.py
```

---

## 🌐 Live Preview (Optional)

> If deployed to Hugging Face or Render, insert link here

---

## 📝 License

MIT License.  
Feel free to use and extend with attribution.

---

## 🙌 Credits

Built with 💬 Transformers, ⚡ FastAPI, 🎨 Gradio, and 🧠 Open Source ML.

