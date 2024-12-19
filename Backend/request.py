import requests

# API URL and file to upload
url = 'http://127.0.0.1:5908/upload'
file_path = 'path_to_your_file.png'

# Open the file in binary mode and send the request
with open(file_path, 'rb') as file:
    files = {'file': file}
    response = requests.post(url, files=files)

# Check response
if response.status_code == 200:
    data = response.json()
    print("File uploaded successfully!")
    print(f"IPFS Hash: {data['ipfs_hash']}")
else:
    print(f"Error: {response.json()}")