@app.route('/generate_thread', methods=['POST'])
def generate_thread():
    try:
        data = request.json
        topic = data.get("topic", "Entrepreneurship")
        subreddits = data.get("subreddits", ["technology", "business"])
        keywords = data.get("keywords", ["AI", "automation", "startup"])
        num_threads = int(data.get("num_threads", 1))
        thread_length = int(data.get("thread_length", 5))

        print(f"Request Received: {data}")  # Log incoming request

        threads = []
        for i in range(num_threads):
            thread_posts = []

            for subreddit in subreddits:
                print(f"Fetching subreddit: {subreddit}")
                posts = fetch_reddit_posts(subreddit, keywords)
                if posts:
                    thread_posts.extend(posts[:thread_length])

            if not thread_posts:
                thread_posts = [f"🔥 {topic} Insight {j+1}" for j in range(thread_length)]  # Fallback if no data found

            threads.append(thread_posts)

        print(f"Generated Threads: {threads}")  # Log generated output
        return jsonify({"threads": threads})

    except Exception as e:
        print(f"Error generating thread: {e}")  # Log the error message
        return jsonify({"error": f"Internal Server Error: {e}"}), 500
