import os
import requests
import jwt
import time
from jwt import JWT
import time
import os


def print_repo_details():

    # Authenticate as the GitHub App
    headers = {
        "Authorization": f"Bearer {generate_jwt(private_key, app_id)}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Use the GitHub REST API to get repository information
    repo_url = f"https://api.github.com/repositories/{os.environ['GITHUB_REPOSITORY_ID']}"
    repo_response = requests.get(repo_url, headers=headers)
    
    if repo_response.status_code == 200:
        repo_data = repo_response.json()
        # Print repository name and language
        print(f"Repository Name: {repo_data['name']}")
        print(f"Repository Language: {repo_data['language']}")
    else:
        print(f"Failed to retrieve repository information. Status code: {repo_response.status_code}")


def generate_jwt(private_key, app_id):
    payload = {
        'iat': int(time.time()),  # Issued at time
        'exp': int(time.time()) + 600,  # JWT expiration time (10 minutes maximum)
        'iss': app_id  # GitHub App's identifier
    }

    # Create JWT
    jwt_instance = JWT()
    encoded_jwt = jwt_instance.encode(payload, private_key, alg='RS256')

    return encoded_jwt

if __name__ == "__main__":
    # Get private key and app ID from GitHub secrets
    private_key = os.environ.get("APP_PRIVATE_KEY").replace('\\n', '\n')
    app_id = int(os.environ.get("APP_ID"))

    jwt_token = generate_jwt(private_key, app_id)
    print(f"JWT:  {jwt_token}")
    print_repo_details()

