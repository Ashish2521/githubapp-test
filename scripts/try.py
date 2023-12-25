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

def get_access_token_details():
    # Authenticate as the GitHub App
    jwt_token = generate_jwt()
    if jwt_token is None:
        print("Authentication failed. Check previous error messages for details.")
        return
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    access_token_url = f"https://api.github.com/app/installations/45427177/access_tokens"

    try:
        access_token_response = requests.post(access_token_url, headers=headers)
        access_token_response.raise_for_status()
        print(access_token_response.status_code)

        if access_token_response.status_code == 201:
            access_token_data = access_token_response.json()
            print(access_token_data)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    # # Use the GitHub REST API to get repository information
    # installation_url = f"https://api.github.com/app/installations"
    # try:
    #     app_id = int(os.environ.get("APP_ID")) 
    #     installation_response = requests.get(installation_url, headers=headers)
    #     installation_response.raise_for_status()
        
    #     if installation_response.status_code == 200:
    #         installation_data = installation_response.json()
    #         installation_id = installation_data[0]['id']
    #         print(installation_id)
    #         access_token_url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    #         jwt_token = generate_jwt()
    #         if jwt_token is None:
    #             print("Authentication failed. Check previous error messages for details.")
    #             return
    #         headers = {
    #             "Authorization": f"Bearer {jwt_token}",
    #             "Accept": "application/vnd.github.v3+json",
    #         }

    #         try:
    #             access_token_response = requests.get(access_token_url, headers=headers)
    #             access_token_response.raise_for_status()

    #             if access_token_response.status_code == 200:
    #                 access_token_data = access_token_response.json()
    #                 print(access_token_data)
    #         except requests.exceptions.RequestException as e:
    #             print(f"Request failed: {e}")
    #     else:
    #         print(f"Failed to retrieve repository information. Status code: {installation_response.status_code}")

    # except requests.exceptions.RequestException as e:
    #     print(f"Request failed: {e}")

if __name__ == "__main__":
    
    # Print repository details
    access_token = get_access_token_details()
