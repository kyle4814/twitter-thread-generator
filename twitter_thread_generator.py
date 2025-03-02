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

    # Ensure multiple threads are generated
    threads = []
    for i in range(num_threads):
        thread = [f"🔥 {topic} Insight {j+1} (Thread {i+1})" for j in range(thread_length)]
        threads.append(thread)

    print("Generated Threads:", threads)  # Debugging
    return jsonify({"threads": threads})

if __name__ == '__main__':
    app.run(debug=True)
