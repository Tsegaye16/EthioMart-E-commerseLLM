from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from utils.telegram_scraper import TelegramScraper
from utils.data_normalizer import DataPreprocessor
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Set directories
RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'json', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/fetch', methods=['POST'])
def fetch_data():
    try:
        data = request.json
        print("Request Data", data)
        channel = data.get("channel")
        if not channel:
            return jsonify({"error": "Channel name is required"}), 400
        
        scraper = TelegramScraper()
        messages = scraper.fetch_messages(channel, limit=200)
        print("Channel message: ", messages)
        scraper.close()

        file_path = os.path.join(RAW_DATA_DIR, f"{channel[1:]}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=4)

        return jsonify({"message": "Data fetched successfully", "path": file_path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/normalize', methods=['POST'])
def normalize_data():
    try:
        # Check if a file is present in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Only JSON and CSV are allowed"}), 400

        # Save the uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(RAW_DATA_DIR, filename)
        file.save(file_path)

        # Normalize the data
        preprocessor = DataPreprocessor(RAW_DATA_DIR, PROCESSED_DATA_DIR)
        preprocessor.preprocess_all()

        return jsonify({"message": "Data normalized successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
