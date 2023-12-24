import os
from github import Github
from github.GithubException import UnknownObjectException

def print_repo_details(app_id, private_key):
    print(f"APP_ID: {app_id}")

    try:
        # Authenticate as the GitHub App using PyGithub
        g = Github(base_url="https://api.github.com", login_or_token=app_id, private_key=private_key)

        # Get repository information
        repo = g.get_repo("Ashish2521/githubapp-test")

        # Print repository details
        print(f"Repository Name: {repo.name}")
        print(f"Repository Language: {repo.language}")
    except UnknownObjectException as e:
        print(f"Failed to retrieve repository information. Error: {str(e)}")

if __name__ == "__main__":
    # Get app ID and private key from GitHub secrets
    app_id = os.environ.get("APP_ID")
    private_key = os.environ.get("APP_PRIVATE_KEY")

    # Print repository details
    print_repo_details(app_id, private_key)
