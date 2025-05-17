from flask import Flask, jsonify, request
from flask_caching import Cache
import time
import random
import logging

app = Flask(__name__)
app.config.from_object("config.Config")

cache = Cache(app)

logging.basicConfig(level=logging.INFO)

@app.route("/")
def home():
    app.logger.info("Home endpoint hit")
    return jsonify(message="Hello from Flask!")

@app.route("/health")
def health():
    return jsonify(status="OK"), 200

@app.route("/heavy")
def heavy():
    app.logger.info("Heavy endpoint simulating load")
    time.sleep(65)  # Simulate a heavy computation or DB call
    return jsonify(result="Heavy computation done!")

@app.route("/cacheme/<param>")
@cache.cached(timeout=30)
def cacheme(param):
    app.logger.info(f"Caching result for: {param}")
    return jsonify(result=f"Processed {param}", random=random.randint(1, 1000))

@app.route("/error")
def error():
    app.logger.error("Intentional error triggered")
    raise Exception("This is a test error for monitoring/logging purposes")

# Error handler
@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.exception("Unhandled exception occurred")
    return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
