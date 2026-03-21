from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from agent import summarize_text, ask_question

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return send_file("index.html")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Please provide text field"}), 400
    result = summarize_text(data["text"])
    return jsonify({"summary": result})

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"error": "Please provide question field"}), 400
    result = ask_question(data["question"])
    return jsonify({"answer": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
