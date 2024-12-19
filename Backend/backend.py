from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import bcrypt
from datetime import datetime
import requests

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# MongoDB connection setup (replace with your MongoDB URI)
MONGO_URI = "mongodb://localhost:27017/mini"
client = MongoClient(MONGO_URI)
db = client.get_database('mini')  # Replace 'mini' with your database name
users_collection = db.users  # Collection to store user data
files_collection = db.files  # Collection to store file metadata

# Pinata API keys
PINATA_API_KEY = "52c60b674ff9c387ca18"
PINATA_SECRET_API_KEY = "177bc828a812c4fc9085a107ebb10afd05328def43501913e2bdcb939993d97f"

@app.route('/')
def home():
    return "Welcome to the Decentralized File Storage Backend!"

# User signup route
@app.route('/signup', methods=['POST'])
def signup_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    print(f"Signup request received: {email}, {password}")  # Debugging output

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    existing_user = users_collection.find_one({"email": email})
    if existing_user:
        return jsonify({"error": "User already exists. Please log in."}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        users_collection.insert_one({"email": email, "password": hashed_password})
        print(f"User {email} registered successfully!")  # Debugging output
    except Exception as e:
        return jsonify({"error": f"Error occurred during signup: {str(e)}"}), 500
    
    return jsonify({"message": "User registered successfully!"}), 201

# User login route (stores email and timestamp in MongoDB)
@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    print(f"Login request received: {email}, {password}")  # Debugging output

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = users_collection.find_one({"email": email})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({"error": "Invalid password"}), 400

    # Store email and timestamp in MongoDB
    try:
        users_collection.update_one({"email": email}, {"$set": {"last_login": datetime.now()}})
        print(f"Login timestamp updated for {email}")  # Debugging output
    except Exception as e:
        return jsonify({"error": f"Error occurred while updating login info: {str(e)}"}), 500

    return jsonify({"message": "Login successful"}), 200

# Upload file to Pinata and save metadata to MongoDB
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "File is required"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY
    }
    files = {"file": file.stream}

    try:
        response = requests.post(url, headers=headers, files=files)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error occurred while uploading to Pinata: {str(e)}"}), 500

    if response.status_code == 200:
        ipfs_hash = response.json()["IpfsHash"]
        try:
            files_collection.insert_one({
                "file_name": file.filename,
                "ipfs_hash": ipfs_hash
            })
            print(f"File {file.filename} uploaded successfully to IPFS")  # Debugging output
        except Exception as e:
            return jsonify({"error": f"Error occurred while saving file metadata: {str(e)}"}), 500
        
        return jsonify({"message": "File uploaded successfully!", "ipfs_hash": ipfs_hash}), 200
    else:
        return jsonify({"error": response.json()}), response.status_code

# Fetch uploaded files
@app.route('/files', methods=['GET'])
def get_files():
    try:
        user_files = files_collection.find()
        files = [{"file_name": file['file_name'], "ipfs_hash": file['ipfs_hash']} for file in user_files]
        print(f"Fetched {len(files)} files.")  # Debugging output
    except Exception as e:
        return jsonify({"error": f"Error occurred while fetching files: {str(e)}"}), 500

    return jsonify(files), 200

# Delete file from Pinata and MongoDB
@app.route('/delete/<ipfs_hash>', methods=['DELETE'])
def delete_file(ipfs_hash):
    file_entry = files_collection.find_one({"ipfs_hash": ipfs_hash})
    if not file_entry:
        return jsonify({"error": "File not found"}), 404

    url = f"https://api.pinata.cloud/pinning/unpin/{ipfs_hash}"
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY
    }

    try:
        response = requests.delete(url, headers=headers)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error occurred while deleting from Pinata: {str(e)}"}), 500

    if response.status_code == 200:
        try:
            files_collection.delete_one({"ipfs_hash": ipfs_hash})
            print(f"File with IPFS hash {ipfs_hash} deleted successfully.")  # Debugging output
        except Exception as e:
            return jsonify({"error": f"Error occurred while deleting file metadata: {str(e)}"}), 500
        
        return jsonify({"message": "File deleted successfully!"}), 200
    else:
        return jsonify({"error": response.json()}), response.status_code

# Run the Flask application
if __name__ == '__main__':
    app.run(port=5908, debug=True)