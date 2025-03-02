from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__, static_folder='static')
CORS(app, resources={r"/*": {"origins": ["https://kyle4814.github.io", "*"]}}, supports_credentials=True)

# Expanded topic database with diverse subjects
TOPIC_DATABASE = {
    "AI": [
        "AI-powered automation saves businesses millions annually.",
        "Neural networks can now predict consumer behavior with 87% accuracy.",
        "GPT-4 has revolutionized content creation for businesses worldwide.",
        "The ethical implications of AI decision-making in healthcare settings.",
    ],
    "Digital Marketing": [
        "SEO is still the #1 driver of free organic traffic for 76% of businesses.",
        "Email marketing generates $42 for every $1 spent on average.",
    ],
    "Sports": [
        "Michael Jordan's mindset: How psychological preparation creates champions.",
        "Recovery science is revolutionizing athletic performance standards.",
    ],
    "History": [
        "The economic factors that contributed to the fall of the Roman Empire.",
        "Archaeological evidence suggests ancient Egyptians used electricity.",
    ],
    "Business": [
        "Problem-solution fit: Why the best businesses solve painful problems.",
        "Recession-proof business models thriving in economic downturns.",
    ]
}

@app.route('/generate_thread', methods=['POST'])
def generate_thread():
    try:
        data = request.json
        topic = data.get("topic", "").strip()
        num_threads = min(int(data.get("num_threads", 1)), 10)
        thread_length = min(int(data.get("thread_length", 5)), 8)
        random_mode = data.get("random_mode", False)

        # Validate input
        num_threads = max(num_threads, 1)
        thread_length = max(thread_length, 1)

        print(f"Request Received: {data}")  # Debug log

        threads = []
        used_insights = set()

        for _ in range(num_threads):
            # Determine the selected topic based on mode and input
            if random_mode or not topic:
                selected_topic = random.choice(list(TOPIC_DATABASE.keys()))
            else:
                # If the user-entered topic isn't in the database, pick a random one
                selected_topic = topic if topic in TOPIC_DATABASE else random.choice(list(TOPIC_DATABASE.keys()))

            # Filter out insights that were already used in previous threads
            available_insights = [
                insight for insight in TOPIC_DATABASE[selected_topic] 
                if insight not in used_insights
            ]

            # If we don't have enough fresh insights, allow repeats
            if len(available_insights) < thread_length:
                a
