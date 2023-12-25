#!/usr/bin/env python3
from jwt import JWT, jwk_from_pem
import time
import sys
import os,requests

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

def print_repo_details():
    # Authenticate as the GitHub App
    jwt_token = generate_jwt()

    if jwt_token is None:
        print("Authentication failed. Check previous error messages for details.")
        return

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    print("Headers:", headers)

    # Use the GitHub REST API to get repository information
    repo_url = f"https://api.github.com/app/installations"
    try:
        repo_response = requests.get(repo_url, headers=headers)
        repo_response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        
        if repo_response.status_code == 200:
            repo_data = repo_response.json()
            print(repo_data)
            # Print repository name and language
            # print(f"Repository Name: {repo_data['name']}")
            # print(f"Repository Language: {repo_data['language']}")
            # print(f"Response body: {repo_response.text}")
        else:
            print(f"Failed to retrieve repository information. Status code: {repo_response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    
    # Print repository details
    print_repo_details()
