#!/bin/bash
python utils/scraper.py
python model/summarizer.py
python utils/ranker.py
uvicorn app.main:app --host 0.0.0.0 --port 8000
