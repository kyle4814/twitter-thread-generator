import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

REDDIT_API_URL = "https://www.reddit.com/r/{}/top.json?limit=5"

def fetch_reddit_posts(subreddit, keywords):
    """Fetch top Reddit posts and filter by keywords."""
    headers = {"User-Agent": "ThreadGeneratorBot"}
    response = requests.get(REDDIT_API_URL.format(subreddit), headers=headers)

    # Log the entire response to debug issues
    print(f"Fetching subreddit: {subreddit}")
    print(f"Response Status: {response.status_code}")

    if response.status_code != 200:
        print(f"Error fetching subreddit {subreddit}: {response.text}")  # Log actual response error
        return []

    try:
        response_json = response.json()
        print(f"Full Response: {response_json}")  # Log full Reddit API response
        posts = response_json.get("data", {}).get("children", [])
    except Exception as e:
        print(f"Error parsing JSON from {subreddit}: {e}")
        return []

    relevant_posts = []
    for post in posts:
        title = post["data"].get("title", "")
        if any(keyword.lower() in title.lower() for keyword in keywords):
            relevant_posts.append(title)

    print(f"Fetched {len(relevant_posts)} matching posts from {subreddit} with keywords {keywords}")
    return relevant_posts
