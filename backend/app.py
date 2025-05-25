from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from dotenv import load_dotenv
import logging
load_dotenv()

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
import os
import logging

UPLOAD_FOLDER = 'uploads'

# Check if path exists and is NOT a directory
if os.path.exists(UPLOAD_FOLDER) and not os.path.isdir(UPLOAD_FOLDER):
    logging.warning(f"'{UPLOAD_FOLDER}' exists and is not a directory. Removing it.")
    os.remove(UPLOAD_FOLDER)  # remove the file

# Now safely make the directory
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    logging.info(f"Upload folder created: {UPLOAD_FOLDER}")
except Exception as e:
    logging.error(f"Failed to create upload folder: {e}")


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Allow up to 16MB uploads

# Ensure upload directory exists





# MongoDB setup
client = MongoClient(os.getenv("MONGO_URI"))
db = client['image_analysis']
collection = db['results']

@app.route('/')
def home():
    return "Server running!"

@app.route('/analyze', methods=['POST'])
def analyze():
    print("Request received at /analyze")

    if 'image' not in request.files:
        print("No image found in request.")
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['image']
    filename = secure_filename(file.filename)
    if not filename:
        print("Filename is empty or unsafe.")
        return jsonify({'error': 'Invalid filename'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    print(f"Image saved to {filepath}")

    # Dummy analysis result
    result = {"filename": filename, "message": "Analysis complete!"}

    # Store result in MongoDB
    collection.insert_one(result)
    print(f"Stored result in MongoDB: {result}")

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
