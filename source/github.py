import requests

def list_github_issues(owner, repo, token=None, state='open'):
    """Fetch issues from GitHub repo."""
    api_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {'Authorization': f'token {token}'} if token else {}
    params = {'state': state, 'per_page': 100}

    all_issues = []
    page = 1

    while True:
        params['page'] = page
        response = requests.get(api_url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch issues: {response.status_code} {response.reason}\n{response.text}")

        issues = response.json()
        if not issues:
            break

        for issue in issues:
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
