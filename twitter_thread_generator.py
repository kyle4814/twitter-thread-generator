from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pydantic import BaseModel, ValidationError
import os
import redis
import json
import logging
import praw
import tweepy
from newsapi import NewsApiClient
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# --- Initialize Services ---
app = Flask(__name__, static_folder='static')
CORS(app, resources={r"/*": {"origins": ["https://kyle4844.github.io", "http://localhost:*"]}})

# Rate Limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri=f"redis://{os.getenv('REDIS_HOST')}:6379/0",
    default_limits=["50/day", "20/hour"]  # Free tier limits
)

# API Clients
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_SECRET'),
    user_agent="twitter-thread-generator"
)

twitter = tweepy.Client(
    bearer_token=os.getenv('TWITTER_BEARER'),
    wait_on_rate_limit=True
)

newsapi = NewsApiClient(api_key=os.getenv('NEWSAPI_KEY'))

# --- Core Logic ---
class ThreadRequest(BaseModel):
    topic: str
    num_threads: int
    thread_length: int
    sources: list  # ["reddit", "twitter", "news"]
    random_mode: bool

def fetch_content(topic: str, source: str):
    try:
        if source == "reddit":
            submissions = reddit.subreddit("all").search(topic, limit=10)
            return [s.title for s in submissions]
        elif source == "twitter":
            tweets = twitter.search_recent_tweets(topic, max_results=10)
            return [t.text for t in tweets.data]
        elif source == "news":
            articles = newsapi.get_everything(q=topic, page_size=10)
            return [a['title'] for a in articles['articles']]
    except Exception as e:
        logging.error(f"{source.upper()} Error: {str(e)}")
        return []

@app.route('/generate_thread', methods=['POST'])
@limiter.limit("10/minute;100/day", deduct_when=lambda r: 'X-User-Tier' not in r.headers)
def generate_thread():
    try:
        data = ThreadRequest(**request.json)
        user_tier = request.headers.get('X-User-Tier', 'free')

        # PRO Check
        if user_tier == "free":
            if data.num_threads > 2: 
                return jsonify(error="Upgrade to PRO for unlimited threads", status="error"), 403
            data.sources = ["reddit"]  # Free users only get Reddit

        # Generate Threads
        threads = []
        for _ in range(data.num_threads):
            insights = []
            for source in data.sources:
                insights += fetch_content(data.topic, source)
            
            threads.append({
                "topic": data.topic,
                "insights": insights[:data.thread_length],
                "sources": data.sources
            })

        return jsonify(threads=threads, status="success")

    except ValidationError as e:
        return jsonify(error=str(e), status="error"), 400
    except Exception as e:
        logging.error(f"Critical Error: {str(e)}")
        return jsonify(error="Server error", status="error"), 500
