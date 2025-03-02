from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# ✅ Fix CORS: Allow requests from GitHub Pages
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "https://kyle4814.github.io"}})

@app.after_request
def add_cors_headers(response):
    """Ensure CORS headers are correctly added."""
    response.headers["Access-Control-Allow-Origin"] = "https://kyle4814.github.io"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

@app.route('/generate_thread', methods=['POST', 'OPTIONS'])
def generate_thread():
    if request.method == "OPTIONS":
        return jsonify({"message": "CORS preflight successful"}), 200

    try:
        data = request.json
        topic = data.get("topic", "").strip()
        num_threads = min(int(data.get("num_threads", 1)), 10)
        thread_length = min(int(data.get("thread_length", 5)), 8)
        random_mode = data.get("random_mode", False)

        threads = []

        for _ in range(num_threads):
            selected_topic = topic if topic in TOPIC_DATABASE else random.choice(list(TOPIC_DATABASE.keys()))
            selected_insights = random.sample(TOPIC_DATABASE[selected_topic], min(thread_length, len(TOPIC_DATABASE[selected_topic])))

            thread = [f"🔥 {selected_topic}: {insight}" for insight in selected_insights]
            threads.append(thread)

        return jsonify({"threads": threads, "status": "success"})

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}", "status": "error"}), 500

if __name__ == '__main__':
    app.run(debug=True)


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

# Function to fetch data from Reddit API
def fetch_reddit_insights(topic):
    headers = {"User-Agent": "TwitterThreadGenerator/1.0"}
    url = f"https://www.reddit.com/r/{topic}/top.json?limit=5"
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            posts = response.json().get("data", {}).get("children", [])
            return [post["data"]["title"] for post in posts][:5]
    except Exception as e:
        print(f"Reddit fetch error: {e}")
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
            if random_mode or not topics:
                selected_topic = random.choice(list(TOPIC_DATABASE.keys()))
            else:
                selected_topic = random.choice(topics) if topics else random.choice(list(TOPIC_DATABASE.keys()))

            available_insights = fetch_reddit_insights(selected_topic) or TOPIC_DATABASE.get(selected_topic, [])
            available_insights = [insight for insight in available_insights if insight not in used_insights]

            if len(available_insights) < thread_length:
                available_insights = TOPIC_DATABASE[selected_topic]

            selected_insights = random.sample(available_insights, min(thread_length, len(available_insights)))
            thread = [f"🔥 {selected_topic}: {insight}" for insight in selected_insights]
            used_insights.update(selected_insights)
            threads.append(thread)

        return jsonify({"threads": threads, "status": "success"})

    except Exception as e:
        print(f"Error generating thread: {e}")
        return jsonify({"error": f"Internal Server Error: {str(e)}", "status": "error"}), 500

if __name__ == '__main__':
    print("✨ Insight Generator server is running!")
    app.run(host='0.0.0.0', port=5000, debug=True)
