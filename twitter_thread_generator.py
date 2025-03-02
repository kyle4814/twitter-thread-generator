from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://kyle4814.github.io", "*"]}}, supports_credentials=True)

@app.route('/generate_thread', methods=['POST'])
def generate_thread():
    try:
        data = request.json
        topic = data.get("topic", "Entrepreneurship")
        num_threads = int(data.get("num_threads", 1))
        thread_length = int(data.get("thread_length", 5))

        print(f"Request Received: {data}")  # Debugging

        threads = []
        for i in range(num_threads):
            thread = [f"🔥 {topic} Insight {j+1} (Thread {i+1})" for j in range(thread_length)]
            threads.append(thread)

        print(f"Generated {len(threads)} threads")  # Debugging log
        return jsonify({"threads": threads})  # Ensure it's a list, not an object

    except Exception as e:
        print(f"Error generating thread: {e}")
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
