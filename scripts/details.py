import os
import requests
from jwt import JWT, jwk_from_pem
import time
import sys

def generate_jwt(app_id, private_key):
    now = int(time.time())
    payload = {
        # Issued at time
        'iat': int(time.time()),
        # JWT expiration time (10 minutes maximum)
        'exp': int(time.time()) + 600,
        # GitHub App's identifier
        'iss': app_id
    }

    # Create JWT
    jwt_instance = JWT()
    encoded_jwt = jwt_instance.encode(payload, private_key, alg='RS256')

    return encoded_jwt

def print_repo_details(app_id, private_key):
    # Authenticate as the GitHub App
    jwt_token = generate_jwt(app_id, private_key)
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Use the GitHub REST API to get repository information
    repo_url = f"https://api.github.com/repos/Ashish2521/githubapp-test"
    repo_response = requests.get(repo_url, headers=headers)
    print(repo_response.text)
    
    if repo_response.status_code == 200:
        repo_data = repo_response.json()
        # Print repository name and language
        print(f"Repository Name: {repo_data['name']}")
        print(f"Repository Language: {repo_data['language']}")
        print(f"Response body: {repo_response.text}")
    else:
        print(f"Failed to retrieve repository information. Status code: {repo_response.status_code}")

if __name__ == "__main__":
    # Get app ID and private key from GitHub secrets
    app_id = int(os.environ.get("APP_ID"))
    private_key = os.environ.get("APP_PRIVATE_KEY").replace('\\n', '\n')

    # Print repository details
    print_repo_details(app_id, private_key)
