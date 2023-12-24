import os
import requests
import jwt
import time

def main():
    private_key = os.environ.get("PRIVATE_KEY")
    app_id = int(os.environ.get("APP_ID"))

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
    now = int(time.time())
    payload = {
        'iat': now,  # Issued at time
        'exp': now + 60,  # JWT expiration time (in seconds)
        'iss': app_id  # GitHub App identifier
    }
    token = jwt.encode(payload, private_key, algorithm='RS256')
    return token

if __name__ == "__main__":
    main()
