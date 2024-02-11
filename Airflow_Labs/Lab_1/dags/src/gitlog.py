import requests


# Function to create a GitHub issue
def create_github_issue(token, title, body):
    """
    Create a GitHub issue in a specific repository.

    Args:
        token (str): GitHub authentication token.
        title (str): Title of the GitHub issue.
        body (str): Body of the GitHub issue.

    Returns:
        bool: True if the issue was created successfully, False otherwise.
    """
    # Define the GitHub API URL for creating issues
    url = f'https://api.github.com/repos/DRAJ6/Airflow-GitHub/issues'

    # Define headers including the authentication token and accept header
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Define the data for the issue, including labels, title, and body
    data = {
        'labels': ["error"],
        'title': title,
        'body': body
    }

    # Send a POST request to create the GitHub issue
    response = requests.post(url, headers=headers, json=data)

    # Check the response status code to determine if the issue was created successfully
    if response.status_code == 201:
        print(f"GitHub issue logged: {response.json()['html_url']}")
        return True
    else:
        print(f"Failed to create GitHub issue. Status code: {response.status_code}")
        return False
