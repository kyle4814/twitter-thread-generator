from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import requests
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": os.getenv('CORS_ORIGINS', 'https://kyle4814.github.io').split(',')}})

# ✅ Topic Database with balanced variety
TOPIC_DATABASE = {
    "AI": [
        "🚀 AI is taking over. Here’s how you can profit before it’s too late!",
        "🤖 Neural networks now predict consumer behavior with 87% accuracy!",
    ],
    "Business": [
        "💰 Recession-proof business models thriving right now! Don’t miss out!",
        "📈 How storytelling creates deep emotional connections with customers!",
    ],
    "Finance": [
        "📊 The ultimate guide to wealth preservation during recessions!",
        "📉 Why 90% of retail traders fail (and how to be in the 10%)",
    ],
}

# ✅ Function to fetch data from external APIs
def fetch_reddit_trends():
    """Fetch top Reddit posts dynamically"""
    headers = {"User-Agent": "TwitterThreadGenerator/1.0"}
    try:
        response = requests.get('https://www.reddit.com/r/popular/top.json?limit=5', headers=headers, timeout=5)
        return [post["data"]["title"] for post in response.json().get("data", {}).get("children", [])]
    except Exception:
        return []

@app.route('/generate_thread', methods=['POST'])
def generate_thread():
    try:
        data = request.json
        topics = [t.strip() for t in data.get("topic", "").split(",")]
        num_threads = min(int(data.get("num_threads", 1)), 10)
        thread_length = min(int(data.get("thread_length", 5)), 8)
        random_mode = data.get("random_mode", False)

        threads = []
        used_insights = set()

        for _ in range(num_threads):
            selected_topic = random.choice(list(TOPIC_DATABASE.keys())) if random_mode else random.choice(topics) if topics else "AI"

            insights = fetch_reddit_trends() or TOPIC_DATABASE.get(selected_topic, [])
            insights = [insight for insight in insights if insight not in used_insights]

            if len(insights) < thread_length:
                insights = TOPIC_DATABASE[selected_topic]

            selected_insights = random.sample(insights, min(thread_length, len(insights)))
            thread = [f"🔥 {selected_topic}: {insight}" for insight in selected_insights]
            used_insights.update(selected_insights)
            threads.append(thread)

        return jsonify({"threads": threads, "status": "success"})

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
