from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://kyle4814.github.io", "*"]}}, supports_credentials=True)

# Sample AI-generated insights (this should be replaced with real data pulling logic)
AI_INSIGHTS = [
    "AI is transforming business in 2025!",
    "Automation is key to scaling online businesses.",
    "AI chatbots are replacing customer service reps.",
    "Use AI to generate unique content in seconds.",
    "AI-powered automation saves businesses millions.",
    "AI-driven social media growth is the future.",
    "How AI is changing e-commerce forever.",
    "The next trillion-dollar industry: AI tools & software."
]

@app.route('/generate_thread', methods=['POST'])
def generate_thread():
    try:
        data = request.json
        topic = data.get("topic", "Entrepreneurship")
        num_threads = int(data.get("num_threads", 1))
        thread_length = int(data.get("thread_length", 5))
        random_mode = data.get("random_mode", False)  # If checked, enable self-seeking AI mode

        print(f"Request Received: {data}")  # Debugging log

        threads = []
        for i in range(num_threads):
            if random_mode:
                thread = random.sample(AI_INSIGHTS, min(thread_length, len(AI_INSIGHTS)))  # Ensure uniqueness
            else:
                thread = [f"🔥 {topic} Insight {j+1} (Thread {i+1})" for j in range(thread_length)]
            
            threads.append(thread)

        print(f"Generated {len(threads)} threads")  # Debugging log
        return jsonify({"threads": threads})

    except Exception as e:
        print(f"Error generating thread: {e}")
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
