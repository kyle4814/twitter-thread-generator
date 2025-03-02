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
                selected_topic = topic if topic in TOPIC_DATABASE else random.choice(list(TOPIC_DATABASE.keys()))

            # Select unique insights for this thread
            available_insights = [insight for insight in TOPIC_DATABASE[selected_topic] if insight not in used_insights]

            if len(available_insights) < thread_length:
                available_insights = TOPIC_DATABASE[selected_topic]

            selected_insights = random.sample(available_insights, min(thread_length, len(available_insights)))
            thread = [f"🔥 {selected_topic}: {insight}" for insight in selected_insights]
            used_insights.update(selected_insights)
            threads.append(thread)

        print(f"Generated {len(threads)} threads successfully")
        return jsonify({"threads": threads, "status": "success"})

    except Exception as e:
        print(f"Error generating thread: {e}")
        return jsonify({"error": f"Internal Server Error: {str(e)}", "status": "error"}), 500

if __name__ == '__main__':
    print("✨ Insight Generator server is running!")
    app.run(debug=True)
