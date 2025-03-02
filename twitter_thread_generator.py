from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import random
import requests
import os
import redis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# ================== CORS CONFIGURATION ==================
CORS(app, resources={
    r"/generate_thread": {
        "origins": "*",
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

# ================== REDIS CACHING ==================
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=os.getenv('REDIS_PORT', 6379),
    db=0
)

# ================== RATE LIMITING ==================
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379/0",
    default_limits=["200 per day", "50 per hour"]
)

# ================== VIRAL CONTENT FRAMEWORKS ==================
VIRAL_FRAMEWORKS = {
    'hook_problem_solution': [
        "🔥 {hook} (But here's what nobody is telling you...)",
        "💔 The REAL problem: {problem}",
        "💡 BREAKTHROUGH: {insight}",
        "🚀 Solution: {solution} (👉 {cta})"
    ],
    'listicle': [
        "🚀 {count} {topic} Secrets Top Experts Won't Tell You:",
        "1️⃣ {point1}",
        "2️⃣ {point2}",
        "3️⃣ {point3}",
        "🔑 The Key: {key_insight} (👉 {cta})"
    ]
}

CTAS = [
    "Grab your FREE guide → [LINK]",
    "Join our premium community → [LINK]",
    "Book your AI consultation → [LINK]"
]

# ================== TRENDING CONTENT FETCHERS ==================
def fetch_reddit_trends():
    cache_key = "reddit_trends"
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    headers = {"User-Agent": "MoneyPrinterAI/1.0"}
    response = requests.get("https://www.reddit.com/r/popular/top.json?limit=15", headers=headers)
    data = response.json().get('data', {}).get('children', [])
    trends = [post['data']['title'] for post in data]
    redis_client.setex(cache_key, 3600, json.dumps(trends))  # Cache for 1 hour
    return trends

# ================== MAIN ENDPOINT ==================
@app.route('/generate_thread', methods=['POST'])
@limiter.limit("10/minute")
def generate_thread():
    try:
        data = request.json
        # [Add improved AI generation logic here]
        
        # Return formatted response with CTA
        return jsonify({
            "threads": formatted_threads,
            "cta": random.choice(CTAS),
            "status": "success"
        })
    
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000))
