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

def get_installation_id(jwt_token):
    # Get installation ID
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    app_installations_url = f"https://api.github.com/app/installations"

    try:
        installations_response = requests.get(app_installations_url, headers=headers)
        installations_response.raise_for_status()

        installations_data = installations_response.json()
        print(installations_data)
        if installations_data and len(installations_data) > 0:
            return installations_data[0]['id']  # Assuming you want the first installation ID
        else:
            print("No installations found.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def get_access_token_details(installation_id, jwt_token):
    # Authenticate as the GitHub App using installation ID
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    access_token_url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"

    try:
        access_token_response = requests.post(access_token_url, headers=headers,params={"permissions": "repo"})
        access_token_response.raise_for_status()

        if access_token_response.status_code == 201:
            access_token_data = access_token_response.json()
            print(access_token_data)
            return access_token_data.get('token')
        else:
            print(f"Failed to obtain access token. Status code: {access_token_response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
def get_repo_details(access_token, owner, repo):
    # Get repository details
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    repo_url = f"https://api.github.com/users/Ashish2521/repos"

    try:
        repo_response = requests.get(repo_url, headers=headers)
        repo_response.raise_for_status()


        if repo_response.status_code == 200:
            repo_data = repo_response.json()
            print(repo_data)
        else:
            print(f"Failed to retrieve repository details. Status code: {repo_response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    # Generate JWT token
    jwt_token = generate_jwt()

    # Get installation ID
    installation_id = get_installation_id(jwt_token)
    if installation_id is not None:
        print(f"Installation ID: {installation_id}")

        # Get access token using installation ID
        access_token = get_access_token_details(installation_id, jwt_token)
        print(f'Access token got !!!!!!!!{access_token}')
        if access_token is not None:
            print(f"Access Token: {access_token}")

            owner = "Ashish2521" 
            repo = "githuapp-test" 
            get_repo_details(access_token, owner, repo)
        else:
            print("Failed to obtain access token.")
    else:
        print("Failed to obtain installation ID.")
