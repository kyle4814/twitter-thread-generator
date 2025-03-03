# twitter_thread_generator.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pydantic import BaseModel
import os
import requests
import redis
import json
import logging
from datetime import timedelta
from textblob import TextBlob  # For sentiment analysis

app = Flask(__name__)
CORS(app)
redis_client = redis.Redis()

# Free News APIs (No keys required)
NEWS_SOURCES = {
    'gnews': 'https://gnews.io/api/v4/top-headlines?q={query}&lang=en&max=10',
    'newsdata': 'https://newsdata.io/api/1/news?apikey=pub_1234567890abcdef&q={query}',
    'innews': 'https://inshortsapi.google.com/news?news_category={query}',
    'contextualweb': 'https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/NewsSearchAPI?q={query}',
    'bingnews': 'https://api.bing.microsoft.com/v7.0/news/search?q={query}',
    'thenewsapi': 'https://api.thenewsapi.com/v1/news/top?api_token=free_token&search={query}',
    'newscatcher': 'https://api.newscatcherapi.com/v2/search?q={query}',
    'guardian': 'https://content.guardianapis.com/search?q={query}&api-key=test',
    'nytimes': 'https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&api-key=test',
    'freenews': 'https://freenewsapi.net/api/v1/news?q={query}'
}

class ThreadRequest(BaseModel):
    topic: str
    num_threads: int
    thread_length: int
    sources: list

@app.route('/generate_thread', methods=['POST'])
@limiter.limit("15/minute")
def generate_thread():
    try:
        data = ThreadRequest(**request.json)
        threads = []
        
        for _ in range(data.num_threads):
            insights = []
            for source in data.sources:
                try:
                    if source == 'reddit':
                        insights += get_reddit_news(data.topic)
                    else:
                        url = NEWS_SOURCES[source].format(query=data.topic)
                        response = requests.get(url)
                        insights += parse_news(response.json(), source)
                except Exception as e:
                    logging.error(f"{source} error: {str(e)}")
            
            # Enhance with AI analysis
            enhanced = enhance_content(insights[:data.thread_length])
            threads.append({"topic": data.topic, "insights": enhanced})
            
        return jsonify(threads=threads)
    
    except Exception as e:
        return jsonify(error=str(e)), 500

def enhance_content(insights):
    enhanced = []
    for text in insights:
        analysis = TextBlob(text)
        hashtags = generate_hashtags(text)
        enhanced.append(f"{text}\n\nSentiment: {analysis.sentiment.polarity:.2f} {hashtags}")
    return enhanced

def generate_hashtags(text):
    keywords = [word for word in text.split() if word.isalnum() and len(word) > 4]
    return ' '.join(f'#{kw}' for kw in keywords[:3])
