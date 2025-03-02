from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import random
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure CORS properly
CORS(app, resources={
    r"/generate_thread": {
        "origins": "*",  # Allow all origins
        "methods": ["POST", "OPTIONS"],  # Allow POST and OPTIONS methods
        "allow_headers": ["Content-Type"]  # Allow Content-Type header
    }
})

# Topic database with diverse subjects
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

# Function to fetch data from NewsAPI
def fetch_news_insights(topic):
    api_key = os.getenv('NEWSAPI_KEY')
    if not api_key:
        return []
        
    url = f"https://newsapi.org/v2/everything?q={topic}&sortBy=popularity&apiKey={api_key}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            return [article["title"] for article in articles][:5]
    except Exception as e:
        print(f"NewsAPI fetch error: {e}")
    return []

# Route to generate Twitter threads
@app.route('/generate_thread', methods=['POST'])
def generate_thread():
    try:
        data = request.json
        topics = [t.strip() for t in data.get("topic", "").split(",") if t.strip()]
        num_threads = min(int(data.get("num_threads", 1)), 10)
        thread_length = min(int(data.get("thread_length", 5)), 8)
        random_mode = data.get("random_mode", False)

        threads = []
        used_insights = set()

        for _ in range(num_threads):
            # Select topic based on user input or random selection
            if random_mode or not topics:
                selected_topic = random.choice(list(TOPIC_DATABASE.keys()))
            else:
                selected_topic = random.choice(topics) if topics else random.choice(list(TOPIC_DATABASE.keys()))

            # Try to fetch insights from Reddit first
            available_insights = fetch_reddit_insights(selected_topic)
            
            # If Reddit fails, try NewsAPI
            if not available_insights:
                available_insights = fetch_news_insights(selected_topic)
            
            # Fallback to our database if external APIs fail
            if not available_insights:
                available_insights = TOPIC_DATABASE.get(selected_topic, [])

            # Filter out previously used insights
            available_insights = [insight for insight in available_insights if insight not in used_insights]
            
            # If we don't have enough unique insights, get more from our database
            if len(available_insights) < thread_length:
                db_insights = [insight for insight in TOPIC_DATABASE.get(selected_topic, []) 
                              if insight not in used_insights]
                available_insights.extend(db_insights)
            
            # Select insights randomly
            selected_insights = random.sample(
                available_insights, 
                min(thread_length, len(available_insights))
            
            # Format the thread
            thread = [f"{insight}" for insight in selected_insights]
            used_insights.update(selected_insights)
            threads.append({"topic": selected_topic, "insights": thread})

        return jsonify({"threads": threads, "status": "success"})

    except Exception as e:
        print(f"Error generating thread: {e}")
        return jsonify({"error": f"Internal Server Error: {str(e)}", "status": "error"}), 500

# Run the Flask app
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('ENV', 'dev').lower() == 'dev'
    print(f"✨ Insight Generator server is running in {os.getenv('ENV', 'dev')} mode!")
    app.run(host='0.0.0.0', port=port, debug=debug)
