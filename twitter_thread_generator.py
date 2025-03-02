from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://kyle4814.github.io", "*"]}}, supports_credentials=True)

# Expanded AI INSIGHTS with diverse topics
TOPIC_DATABASE = {
    "AI": [
        "AI-powered automation saves businesses millions.",
        "Automation is key to scaling online businesses.",
        "AI-driven social media growth is the future.",
        "The next trillion-dollar industry: AI tools & software.",
        "AI chatbots are replacing customer service reps."
    ],
    "Digital Marketing": [
        "SEO is still the #1 driver of free organic traffic.",
        "Email marketing has the highest ROI in digital marketing.",
        "YouTube automation is an untapped goldmine.",
        "TikTok ads are converting better than Facebook ads.",
        "Content repurposing is the best-kept secret for scaling."
    ],
    "Sports": [
        "Michael Jordan's mindset is what separated him from the rest.",
        "The 2024 Olympics will see record-breaking performances.",
        "Why endurance training is essential for any athlete.",
        "The rise of AI-assisted coaching in professional sports.",
        "Strength training vs cardio: Which is better?"
    ],
    "History": [
        "The fall of the Roman Empire holds lessons for modern society.",
        "Ancient civilizations had advanced technology beyond their time.",
        "World War II changed global politics forever.",
        "The impact of the Renaissance on modern science.",
        "How historical events influence today's financial markets."
    ],
    "Business": [
        "The best businesses solve painful problems.",
        "Recession-proof businesses to start in 2025.",
        "How to scale from $10K to $100K/month in revenue.",
        "Why brand storytelling is crucial in marketing.",
        "Top industries poised for explosive growth."
    ],
}

@app.route('/generate_thread', methods=['POST'])
def generate_thread():
    try:
        data = request.json
        topic = data.get("topic", "AI")  # Default to AI if no topic is entered
        num_threads = int(data.get("num_threads", 1))
        thread_length = int(data.get("thread_length", 5))
        random_mode = data.get("random_mode", False)  # If checked, enable AI self-seeking mode

        print(f"Request Received: {data}")  # Debugging log

        threads = []

        for i in range(num_threads):
            if random_mode:
                # Select a completely random topic and pull its insights
                selected_topic = random.choice(list(TOPIC_DATABASE.keys()))
                thread = random.sample(TOPIC_DATABASE[selected_topic], min(thread_length, len(TOPIC_DATABASE[selected_topic])))
            else:
                # If topic exists in database, use it. Otherwise, generate placeholders.
                if topic in TOPIC_DATABASE:
                    thread = random.sample(TOPIC_DATABASE[topic], min(thread_length, len(TOPIC_DATABASE[topic])))
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
