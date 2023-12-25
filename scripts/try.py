#!/usr/bin/env python3
from jwt import JWT, jwk_from_pem
import time
import os
import requests

def generate_jwt():
    # Get PEM file path
    pem = os.path.join(os.path.dirname(__file__), "private-key.pem")

    # Get the App ID
    app_id = int(os.environ.get("APP_ID"))

    # Open PEM
    with open(pem, 'rb') as pem_file:
        signing_key = jwk_from_pem(pem_file.read())

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
    encoded_jwt = jwt_instance.encode(payload, signing_key, alg='RS256')
    return encoded_jwt

def get_installation_access_token(jwt_token):
    installation_url = "https://api.github.com/app/installations"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        installation_response = requests.post(installation_url, headers=headers)
        installation_response.raise_for_status()

        if installation_response.status_code == 201:
            installation_data = installation_response.json()
            return installation_data.get("access_token")
        else:
            print(f"Failed to get installation access token. Status code: {installation_response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def print_repo_details(access_token):
    if access_token is None:
        print("Failed to get installation access token. Check previous error messages for details.")
        return

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Use the GitHub REST API to get repository information
    repo_url = "https://api.github.com/repos/:owner/:repo"  # Replace with the actual repository URL
    try:
        repo_response = requests.get(repo_url, headers=headers)
        repo_response.raise_for_status()

        if repo_response.status_code == 200:
            repo_data = repo_response.json()
            print("Repository Details:")
            print(f"Repository Name: {repo_data['name']}")
            print(f"Repository Language: {repo_data['language']}")
        else:
            print(f"Failed to retrieve repository information. Status code: {repo_response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    # Step 1: Generate JWT token
    jwt_token = generate_jwt()

    # Step 2: Get installation access token
    access_token = get_installation_access_token(jwt_token)

    # Step 3: Print repository details using the installation access token
    print_repo_details(access_token)
