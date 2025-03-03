from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pydantic import BaseModel, ValidationError
import requests
import redis
import json
import logging
from textblob import TextBlob
from datetime import timedelta

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Redis
redis_client = redis.Redis()

# Initialize Rate Limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri="memory://",  # Use in-memory storage for simplicity
    default_limits=["10 per minute"]
)

# Free News API Endpoints
NEWS_APIS = {
    'gnews': 'https://gnews.io/api/v4/search?q={query}&lang=en',
    'innews': 'https://inshortsapi.google.com/news?news_category={query}',
    'contextualweb': 'https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/NewsSearchAPI?q={query}',
    'thenewsapi': 'https://api.thenewsapi.com/v1/news/top?search={query}',
    'freenews': 'https://freenewsapi.net/api/v1/news?q={query}'
}

# Request validation model
class ThreadRequest(BaseModel):
    topic: str
    num_threads: int
    thread_length: int
    sources: list

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found", "status": "error"}), 404

@app.errorhandler(429)
def rate_limit_exceeded(error):
    return jsonify({"error": "Rate limit exceeded", "status": "error"}), 429

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error", "status": "error"}), 500

# Main endpoint
@app.route('/generate_thread', methods=['POST'])
@limiter.limit("10 per minute")
def generate_thread():
    try:
        # Validate request
        data = ThreadRequest(**request.json)
        
        # Check user tier (example: free vs. pro)
        user_tier = request.headers.get('X-User-Tier', 'free')
        if user_tier == 'free' and data.num_threads > 2:
            return jsonify({"error": "Upgrade to PRO for more threads", "status": "error"}), 403

        # Generate threads
        threads = []
        for _ in range(data.num_threads):
            insights = []
            for source in data.sources:
                try:
                    if source == 'reddit':
                        insights += get_reddit_news(data.topic)
                    else:
                        url = NEWS_APIS[source].format(query=data.topic)
                        response = requests.get(url, timeout=5)
                        insights += parse_news(response.json(), source)
                except Exception as e:
                    logging.warning(f"{source} error: {str(e)}")
            
            # Enhance with AI analysis
            enhanced = enhance_content(insights[:data.thread_length])
            threads.append({"topic": data.topic, "insights": enhanced})
        
        return jsonify({"threads": threads, "status": "success"})
    
    except ValidationError as e:
        return jsonify({"error": str(e), "status": "error"}), 400
    except Exception as e:
        logging.error(f"Error generating thread: {str(e)}")
        return jsonify({"error": "Internal server error", "status": "error"}), 500

# Helper functions
def get_reddit_news(query):
    # Placeholder for Reddit API integration
    return [f"Reddit post about {query}"]

def parse_news(data, source):
    # Parse news API responses
    if source == 'gnews':
        return [article['title'] for article in data.get('articles', [])]
    elif source == 'innews':
        return [article['title'] for article in data.get('data', [])]
    return []

def enhance_content(insights):
    # Add sentiment analysis and hashtags
    enhanced = []
    for text in insights:
        analysis = TextBlob(text)
        hashtags = ' '.join(f'#{word}' for word in text.split() if len(word) > 4)[:100]
        enhanced.append(f"{text}\n\nSentiment: {analysis.sentiment.polarity:.2f} {hashtags}")
    return enhanced

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
