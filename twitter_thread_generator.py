import threading
import time
import requests

def keep_alive():
    """Ping the API every 5 minutes to prevent Railway from sleeping."""
    while True:
        try:
            requests.get("https://web-production-fe14e.up.railway.app/generate_thread")
            print("Pinged Railway to keep alive.")
        except Exception as e:
            print(f"Error pinging Railway: {e}")
        time.sleep(300)  # Wait 5 minutes

# Start Keep-Alive Thread
threading.Thread(target=keep_alive, daemon=True).start()
