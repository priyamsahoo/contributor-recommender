import requests
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import json

load_dotenv()

def parse_github_url(repo_url):
    """Extracts the owner and repository name from a GitHub URL."""
    parsed = urlparse(repo_url)
    path_parts = parsed.path.strip('/').split('/')
    if len(path_parts) < 2:
        raise ValueError("Invalid GitHub URL format. Example: https://github.com/owner/repo")
    owner, repo = path_parts[:2]
    return owner, repo

def list_github_issues(repo_url, state='open', token=None):
    """Lists issues from the GitHub repo."""
    owner, repo = parse_github_url(repo_url)
    api_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'

    params = {
        'state': state,
        'per_page': 100,
    }

    all_issues = []
    page = 1

    while True:
        params['page'] = page
        response = requests.get(api_url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch issues: {response.status_code} {response.reason}")
            print(response.json())
            break

        issues = response.json()
        if not issues:
            break

        for issue in issues:
            # Ignore pull requests (they also show up in /issues endpoint)
            if 'pull_request' in issue:
                continue
            all_issues.append({
                'number': issue['number'],
                'title': issue['title'],
                'body': issue.get('body', ''),
                'created_at': issue['created_at'],
                'user': issue['user']['login'],
                'labels': [label['name'] for label in issue.get('labels', [])]
            })
        page += 1

    return all_issues

def save_issues_to_file(issues, filename="issues.json"):
    """Saves issues to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(issues, f, indent=4)
    print(f"\nSaved {len(issues)} issues to '{filename}'")

if __name__ == "__main__":
    repo_url = input("Enter GitHub repo URL to fetch issues from: ")
    token = os.getenv("GITHUB_TOKEN")
    try:
        issues = list_github_issues(repo_url, token=token)
        save_issues_to_file(issues)
    except Exception as e:
        print(f"Error: {e}")
