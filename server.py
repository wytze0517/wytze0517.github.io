"""
Tiny local server that takes a question from the web page and forwards it
to a locally running LM Studio model, then returns the answer.

Run this on the same machine where LM Studio runs.

Setup:
    1. Install LM Studio:          https://lmstudio.ai
    2. Load the model:             google/gemma-4-e4b (in the LM Studio UI)
    3. Start the local server:     LM Studio -> Developer tab -> "Start Server"
                                    (default: http://localhost:1234)
    4. Install deps:               pip install flask flask-cors requests
    5. Run this server:            python server.py
    6. In another terminal:        ngrok http 5000
    7. Copy the ngrok https URL (e.g. https://abcd1234.ngrok-free.app)
       and paste it into index.html (or into the box on the page itself).
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # allow requests from any origin (GitHub Pages, etc.) - fine for a test

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "google/gemma-4-e4b"  # must match the model name shown in LM Studio


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True)
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        resp = requests.post(
            LM_STUDIO_URL,
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": "user", "content": question}
                ],
                "temperature": 0.7,
                "stream": False,
            },
            timeout=120,
        )
        resp.raise_for_status()
        answer = resp.json()["choices"][0]["message"]["content"].strip()
        return jsonify({"answer": answer})
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Could not reach LM Studio. Is the local server started? (Developer tab -> Start Server)"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "LLM proxy server is running"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
