import time
import unittest
from flask_testing import TestCase
from app import app, cache
from config import Config

class TestingConfig(Config):
    TESTING = True
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 1

class FlaskAppTestCase(TestCase):
    def create_app(self):
        app.config.from_object(TestingConfig)
        return app

    def setUp(self):
        cache.clear()

    def tearDown(self):
        pass

    def test_home_endpoint(self):
        resp = self.client.get("/")
        self.assert200(resp)
        data = resp.get_json()
        self.assertIn("message", data)
        self.assertIn("Hello from Flask v2 deployed via ci-cd pipeline", data["message"])

    def test_health_endpoint(self):
        resp = self.client.get("/health")
        self.assert200(resp)
        self.assertEqual(resp.get_json(), {"status": "OK"})

    def test_bigjson_endpoint(self):
        resp = self.client.get("/bigjson")
        self.assert200(resp)
        data = resp.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2000)
        self.assertEqual(data[0]["item"], 0)
        self.assertEqual(data[-1]["item"], 1999)

    def test_error_endpoint(self):
        resp = self.client.get("/error")
        self.assertStatus(resp, 500)
        data = resp.get_json()
        self.assertIn("error", data)

    def test_heavy_placeholder(self):
        # Monkey-patch time.sleep to avoid 65s delay
        original_sleep = time.sleep
        try:
            time.sleep = lambda x: None
            resp = self.client.get("/heavy")
            self.assert200(resp)
            self.assertIn("result", resp.get_json())
        finally:
            time.sleep = original_sleep


if __name__ == "__main__":
    unittest.main()
