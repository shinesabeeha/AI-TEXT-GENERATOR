from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()
import os
print("ENV VALUE:", os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")
print("API KEY:", api_key)  # Debug check

if not api_key:
    raise ValueError("API key is missing. Check your .env file.")

# Configure Gemini
genai.configure(api_key=api_key)

# Use correct model
model = genai.GenerativeModel("gemini-2.5-flash")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()

        if not data or "prompt" not in data:
            return jsonify({"error": "Prompt is required"}), 400

        prompt = data["prompt"]

        response = model.generate_content(prompt)

        return jsonify({"response": response.text})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)