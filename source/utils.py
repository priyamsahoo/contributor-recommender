from urllib.parse import urlparse
import json

def parse_github_url(repo_url):
    parsed = urlparse(repo_url)
    parts = parsed.path.strip('/').split('/')
    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL format. Expected: https://github.com/owner/repo")
    return parts[0], parts[1]

def save_issues_to_file(issues, filename="issues.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(issues, f, indent=4)
    print(f"Saved {len(issues)} issues to '{filename}'")
