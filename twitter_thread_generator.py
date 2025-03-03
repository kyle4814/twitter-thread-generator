from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pydantic import BaseModel
import requests
import redis
import logging
from textblob import TextBlob
from newspaper import Article
import nltk

nltk.download('punkt')

app = Flask(__name__)
CORS(app)
redis_client = redis.Redis()

# Free News API Endpoints
NEWS_APIS = {
    'gnews': 'https://gnews.io/api/v4/search?q={query}&lang=en',
    'innews': 'https://inshortsapi.google.com/news?news_category={query}',
    'contextualweb': 'https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/NewsSearchAPI?q={query}',
    'thenewsapi': 'https://api.thenewsapi.com/v1/news/top?search={query}',
    'freenews': 'https://freenewsapi.net/api/v1/news?q={query}'
}

class ThreadRequest(BaseModel):
    topic: str
    platform: str = 'twitter'
    num_threads: int = 1

@app.route('/generate', methods=['POST'])
@limiter.limit("10/minute")
def generate():
    data = ThreadRequest(**request.json)
    content = get_content(data.topic)
    optimized = optimize_content(content, data.platform)
    return jsonify(optimized)

def get_content(topic):
    cached = redis_client.get(f"news:{topic}")
    if cached: return json.loads(cached)
    
    articles = []
    for api, url in NEWS_APIS.items():
        try:
            response = requests.get(url.format(query=topic), timeout=3)
            articles += parse_articles(response.json())
        except Exception as e:
            logging.warning(f"API {api} failed: {str(e)}")
    
    enriched = [enrich_text(a) for a in articles[:10]]
    redis_client.setex(f"news:{topic}", 3600, json.dumps(enriched))
    return enriched

def enrich_text(text):
    analysis = TextBlob(text)
    article = Article(text[:5000])
    article.download()
    article.parse()
    return {
        'text': text,
        'sentiment': analysis.sentiment.polarity,
        'keywords': article.keywords[:3],
        'summary': article.summary
    }

def optimize_content(content, platform):
    rules = {'twitter': 280, 'linkedin': 700}
    return [{
        'content': f"{item['summary'][:rules[platform]]}",
        'hashtags': ' '.join(f'#{kw}' for kw in item['keywords'])
    } for item in content]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
