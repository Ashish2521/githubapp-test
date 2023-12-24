import os
import requests
import jwt
import time

def generate_jwt(app_id, private_key_path):
    now = int(time.time())
    payload = {
        'iat': int(time.time()),
        'exp': int(time.time()) + 600,
        'iss': app_id
    }

    with open(private_key_path, 'r') as f:
        private_key = f.read()

    encoded_jwt = jwt.encode(payload, private_key, algorithm='RS256')

    return encoded_jwt

def print_repo_details(app_id, private_key_path):
    print(f"APP_ID: {app_id}")
    print(f"Private Key Path: {private_key_path}")

    # Authenticate as the GitHub App
    jwt_token = generate_jwt(app_id, private_key_path)
    print(f"Generated JWT Token: {jwt_token}")

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Use the GitHub REST API to get repository information
    repo_url = f"https://api.github.com/repos/Ashish2521/githubapp-test"
    repo_response = requests.get(repo_url, headers=headers)
    print(f"Repository API Response: {repo_response.text}")

    if repo_response.status_code == 200:
        repo_data = repo_response.json()
        print(f"Repository Name: {repo_data['name']}")
        print(f"Repository Language: {repo_data['language']}")
    else:
        print(f"Failed to retrieve repository information. Status code: {repo_response.status_code}")

if __name__ == "__main__":
    # Get app ID and private key path
    app_id = int(os.environ.get("APP_ID"))
    private_key_path = "details-test.2023-12-24.private-key (1)"  # Adjust this if your file has a different name or location

    # Print repository details
    print_repo_details(app_id, private_key_path)
