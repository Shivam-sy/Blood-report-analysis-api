from flask import Flask, request, jsonify
from extractor import extract_text_from_pdf
from predictor import analyze_report
from flask_cors import CORS
import os

print("🚀 Starting Blood Report API...")

app = Flask(__name__)

# ✅ Allow local + deployed frontend
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://127.0.0.1:5501",
            "http://localhost:5501",
            "https://your-vercel-app.vercel.app"  # replace later
        ]
    }
})

@app.route('/')
def home():
    return jsonify({
        "status": "success",
        "message": "Blood Report AI API is running"
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 🔥 Check file exists
        if 'file' not in request.files:
            return jsonify({
                "status": "error",
                "message": "No file uploaded"
            }), 400

        file = request.files['file']

        # 🔥 Check file name
        if file.filename == '':
            return jsonify({
                "status": "error",
                "message": "Empty file name"
            }), 400

        # 🔥 Extract text
        text = extract_text_from_pdf(file)

        # Debug (optional)
        print("📄 Extracted text preview:", text[:200])

        # 🔥 Analyze
        result = analyze_report(text)

        return jsonify(result)

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# ✅ Required for Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)