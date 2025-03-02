from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Sample Twitter thread generator function
@app.route('/generate_thread', methods=['POST'])
def generate_thread():
    data = request.json
    topic = data.get("topic", "AI Business Ideas")

    thread = [
        f"🚀 Top {topic} trends in 2025:",
        "1. AI-powered content automation 🤖",
        "2. No-code business tools 💼",
        "3. Subscription-based knowledge products 📚",
        "4. Micro SaaS businesses 💡",
        "5. Monetizing personal brands 🏆",
        "Want more? Follow me for daily insights! 🔥"
    ]

    return jsonify({"thread": thread})

if __name__ == '__main__':
    app.run(debug=True)
