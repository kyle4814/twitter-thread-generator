import unittest
from twitter_thread_generator import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_generate_thread(self):
        response = self.app.post('/generate_thread', json={
            "topic": "AI",
            "num_threads": 1,
            "thread_length": 5,
            "random_mode": False
        })
        self.assertEqual(response.status_code, 200)

def test_generate_thread(self):
    response = self.app.post('/generate_thread', json={
        "topic": "AI",
        "num_threads": 1,
        "thread_length": 5,
        "random_mode": False
    })
    self.assertEqual(response.status_code, 200)
    self.assertIn('threads', response.get_json())
