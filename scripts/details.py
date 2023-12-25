import os
import requests
import jwt
import time
import sys
import datetime

def generate_jwt(app_id, private_key):
    now = int(datetime.datetime.now().timestamp())
    payload = {
        "iat": now - 60,
        "exp": now + 60 * 8,  # expire after 8 minutes
        "iss": app_id
    }

    encoded_jwt = jwt.encode(payload, private_key, algorithm='RS256')

    return encoded_jwt

def print_repo_details(app_id, private_key):
    print(f"APP_ID: {app_id}")

    # Authenticate as the GitHub App
    jwt_token = generate_jwt(app_id, private_key)
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    print(f"Headers: {headers}")

    # Use the GitHub REST API to get repository information
    repo_url = f"https://api.github.com/repos/Ashish2521/githubapp-test"
    try:
        repo_response = requests.get(repo_url, headers=headers)
        repo_response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        
        if repo_response.status_code == 200:
            repo_data = repo_response.json()
            # Print repository name and language
            print(f"Repository Name: {repo_data['name']}")
            print(f"Repository Language: {repo_data['language']}")
            print(f"Response body: {repo_response.text}")
        else:
            print(f"Failed to retrieve repository information. Status code: {repo_response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    # Check authenticated user
    authenticated_user_url = "https://api.github.com/user"
    user_response = requests.get(authenticated_user_url, headers=headers)

    if user_response.status_code == 200:
        user_data = user_response.json()
        print(f"Authenticated User: {user_data['login']}")
    else:
        print(f"Failed to retrieve authenticated user. Status code: {user_response.status_code}")
        print(f"Response body: {user_response.text}")

if __name__ == "__main__":
    # Get app ID and private key from GitHub secrets
    app_id = int(os.environ.get("APP_ID"))
    private_key = os.environ.get("APP_PRIVATE_KEY")

    # Print repository details
    print_repo_details(app_id, private_key)
