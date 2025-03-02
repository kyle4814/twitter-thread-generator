from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pydantic import BaseModel, ValidationError
import random
import requests
import os
import redis
import json
import logging
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# ================== CORS CONFIG (MISSILE-LOCKED EDITION) ==================
CORS(app, resources={
    r"/generate_thread": {
        "origins": ["https://kyle4814.github.io"],  # 4814 NOT 4844
        # ... keep other configs ...
    }
})

# Update manual OPTIONS handler too
@app.route('/generate_thread', methods=['OPTIONS'])
def options_handler():
    return '', 204, {
        'Access-Control-Allow-Origin': 'https://kyle4814.github.io',  # FIXED
        # ... rest unchanged ...
    }

# Initialize Redis
    host=os.getenv('REDIS_HOST', 'redis'),  # Railway uses 'redis' hostname
    port=os.getenv('REDIS_PORT', 6379),
    password=os.getenv('REDIS_PASSWORD', '')  # Add this line
)

# Configure rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri="memory://",  # <-- Use in-memory storage
    default_limits=["200 per day", "50 per hour"]
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Request validation model
class ThreadRequest(BaseModel):
    topic: str
    num_threads: int
    thread_length: int
    random_mode: bool

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found", "status": "error"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error", "status": "error"}), 500

# Redis caching functions
def get_cached_response(key):
    cached = redis_client.get(key)
    return json.loads(cached) if cached else None

def set_cached_response(key, data, ttl=3600):  # Cache for 1 hour
    redis_client.setex(key, timedelta(seconds=ttl), json.dumps(data))

# Main endpoint
@app.route('/generate_thread', methods=['POST'])
@limiter.limit("10/minute")
def generate_thread():
    try:
        # Validate request
        data = ThreadRequest(**request.json)
        
        # Check user tier (example: free vs. pro)
        user_tier = request.headers.get('X-User-Tier', 'free')
        if user_tier == 'free' and data.num_threads > 2:
            return jsonify({"error": "Upgrade to PRO for more threads", "status": "error"}), 403

        # Generate threads (replace with your logic)
        threads = [{"topic": data.topic, "insights": ["Insight 1", "Insight 2"]}]
        
        return jsonify({
            "threads": threads,
            "status": "success"
        })
    
    except ValidationError as e:
        return jsonify({"error": str(e), "status": "error"}), 400
    except Exception as e:
        logger.error(f"Error generating thread: {e}")
        return jsonify({"error": "Internal server error", "status": "error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000))
