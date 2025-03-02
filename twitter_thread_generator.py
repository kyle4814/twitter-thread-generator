import random
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# Predefined viral thread templates for different topics
thread_templates = {
    "AI Business Ideas": [
        "AI is taking over in 2025. Here's how you can start an AI business today:",
        "1. AI-Powered Chatbots for Small Businesses 💬",
        "2. Automated Content Writing with AI 📝",
        "3. AI Stock Market Prediction 📈",
        "4. AI-Based Resume & Cover Letter Generator 🧑‍💼",
        "5. AI Course Creation and Selling 🎓",
        "Want to start an AI business? Follow me for more insights! 🚀"
    ],
    "Money Hacks": [
        "Making money is a game. If you're not winning, you're playing it wrong. Here's how to fix that:",
        "1. Automate your income with digital products 💰",
        "2. Use other people’s money to grow (OPM strategy) 💵",
        "3. Turn your knowledge into a paid community 🏆",
        "4. Set up a faceless TikTok cash cow 🏗️",
        "5. Invest in cash-flowing assets 📊",
        "Want more money hacks? Hit that follow button! ⚡"
    ]
}

@app.route('/generate_thread', methods=['POST'])
def generate_thread():
    data = request.json
    topic = data.get("topic", "AI Business Ideas")
    
    if topic in thread_templates:
        thread = thread_templates[topic]
    else:
        thread = ["Here's how you can win big in 2025:"] + [f"{i}. Random strategy {random.randint(1, 100)}" for i in range(1, 6)]
    
    return jsonify({"thread": thread})

if __name__ == '__main__':
    app.run(debug=True)
