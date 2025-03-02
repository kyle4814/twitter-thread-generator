from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/generate_thread', methods=['POST'])
def generate_thread():
    data = request.json
    topic = data.get("topic", "Entrepreneurship")
    num_threads = int(data.get("num_threads", 1))
    thread_length = int(data.get("thread_length", 5))
    sections = int(data.get("sections", 1))

    # Ensure we generate multiple threads
    threads = []
    for _ in range(num_threads):
        thread = [f"🔥 {topic} Insight {i+1}" for i in range(thread_length)]
        threads.append(thread)

    return jsonify({"threads": threads})

if __name__ == '__main__':
    app.run(debug=True)
