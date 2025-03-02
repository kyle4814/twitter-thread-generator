from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/generate_thread', methods=['POST'])
def generate_thread():
    data = request.json
    topic = data.get("topic", "Entrepreneurship")

    # Ensure valid input
    if not topic:
        return jsonify({"error": "Missing required parameters"}), 400

    # Example thread generation
    threads = [[
        f"🔥 {topic} Insight 1",
        f"🔥 {topic} Insight 2",
        f"🔥 {topic} Insight 3",
        f"🔥 {topic} Insight 4",
        f"🔥 {topic} Insight 5"
    ]]

    return jsonify({"threads": threads})

if __name__ == '__main__':
    app.run(debug=True)
