import os
import requests
import jwt
import time

def generate_jwt(app_id, private_key):
    now = int(time.time())
    payload = {
        'iat': now,
        'exp': now + 600,  # JWT expiration time (10 minutes maximum)
        'iss': app_id
    }

    encoded_jwt = jwt.encode(payload, private_key, algorithm='RS256')

    return encoded_jwt

def print_repo_details(app_id, private_key):
    # Authenticate as the GitHub App
    jwt_token = generate_jwt(app_id, private_key)
    print(f"JWT Token: {jwt_token}")
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Use the GitHub REST API to get repository information
    repo_url = f"https://api.github.com/repositories/githubapp-test"
    repo_response = requests.get(repo_url, headers=headers)
    
    if repo_response.status_code == 200:
        repo_data = repo_response.json()
        # Print repository name and language
        print(f"Repository Name: {repo_data['name']}")
        print(f"Repository Language: {repo_data['language']}")
    else:
        print(f"Failed to retrieve repository information. Status code: {repo_response.status_code}")

if __name__ == "__main__":
    # Get app ID and private key from GitHub secrets
    app_id = int(os.environ.get("APP_ID"))
    private_key = os.environ.get("APP_PRIVATE_KEY").replace('\\n', '\n')

    # Print repository details
    print_repo_details(app_id, private_key)
