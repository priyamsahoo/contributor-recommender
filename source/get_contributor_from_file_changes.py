import requests
import json
import os
from datetime import datetime, timezone

from source.utils import filter_human_users

def search_project_code_file(token: str, query: str, owner: str, repo: str) -> dict:
    """
    Search GitHub code via the GitHub API.

    :param token: GitHub personal access token
    :param query: Search term (e.g. "auto-completion")
    :param repo: Repository in "owner/repo" format (e.g. "ansible/vscode-ansible")
    :return: Parsed JSON response from the API
    """

    url = "https://api.github.com/search/code"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    # params = {

    #     "q": query,
    #     # "q": f"repo:{repo}+in:file+{query}"
    #     "in": "file",
    # }

    params = {
        "q": f"{query} in:file,path repo:{owner}/{repo}"
    }

    # "q": f"repo:{repo}+in:file+{query}"

    response = requests.get(url, headers=headers, params=params)
    # print(response.request.url)
    response.raise_for_status()  # raises an error for 4xx/5xx responses
    return response.json()


def filter_code_paths(items, allowed_exts=None, limit=5):
    if allowed_exts is None:
        allowed_exts = {
            ".py", ".java", ".c", ".cpp", ".js", ".ts",
            ".rb", ".go", ".cs", ".php", ".rs", ".swift", ".kt"
        }

    filtered = []
    for item in items:
        path = item.get("path", "")
        ext = os.path.splitext(path)[1].lower()
        if ext in allowed_exts:
            filtered.append(path)
            if len(filtered) >= limit:
                break

    return filtered


def find_contributors_from_file_data(token, keywords_file, owner, repo):

    # with open(keywords_file, 'r', encoding='utf-8') as f:
    #     entries = json.load(f)
    # kws = set()
    # for e in entries:
    #     kws.update(e.get("keywords", []))
    # keyword_doc = " ".join(kws).lower().split()

    with open(keywords_file, 'r', encoding='utf-8') as f:
        entries = json.load(f)
    keywords = []
    for e in entries:
        keywords.extend(e.get("keywords", []))

    # Remove duplicates while preserving order
    unique_keywords = list(dict.fromkeys(keywords))

    # print(keyword_doc)

    query = unique_keywords[0]
    # query = 'auto-completion'

    print("keyword searching ->", query)
    result = search_project_code_file(token, query, owner, repo)
    # print(result.get("items", []))
    
    # filter the code files
    items = result.get("items", [])
    code_files = filter_code_paths(items, limit=5)
    
    contributors = rank_contributors(token, owner, repo, code_files, commit_limit=20, top_n=5)
    return contributors
    


    # for i in range(0,3):
    #     query = keyword_doc[i]
    #     print("keyword searching ->", query)
    #     result = search_project_code_file(token, query, repo)
    #     print(result)
    #     print()

    # pass


def rank_contributors(token, owner, repo, file_paths, commit_limit=100, top_n=5):
    """
    Fetches up to `commit_limit` most recent commits touching any of the given `file_paths`,
    aggregates authors by number of commits and recency, then returns the top_n contributor logins.
    
    :param owner:       Repository owner (e.g. "ansible")
    :param repo:        Repository name (e.g. "vscode-ansible")
    :param token:       GitHub personal access token
    :param file_paths:  List of file paths to fetch commits for
    :param commit_limit:Max number of commits (across all files) to consider (default 100)
    :param top_n:       How many top contributors to return (default 5)
    :return:            List of top_n contributor logins, sorted by combined score
    """
    headers = {
        "Accept":              "application/vnd.github+json",
        "Authorization":       f"Bearer {token}",
        "X-GitHub-Api-Version":"2022-11-28"
    }

    # 1) Collect all commits touching any of the given files
    all_commits = []
    for path in file_paths:
        url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        params = {"path": path, "per_page": commit_limit}
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        all_commits.extend(resp.json())

    # 2) Sort by commit date descending and take top `commit_limit`
    def commit_date(c):
        # parse ISO8601 date, falling back to author date
        date_str = c["commit"]["author"]["date"]
        # replace 'Z' with '+00:00' for fromisoformat
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    
    all_commits.sort(key=commit_date, reverse=True)
    top_commits = all_commits[:commit_limit]

    # 3) Aggregate per-author counts and recency weights
    now = datetime.now(timezone.utc)
    author_stats = {}
    for c in top_commits:
        # prefer GitHub login if available, otherwise use author name
        author_info = c.get("author")
        login = author_info["login"] if author_info else c["commit"]["author"]["name"]
        
        # count
        stats = author_stats.setdefault(login, {"count": 0, "recency_score": 0.0})
        stats["count"] += 1
        
        # recency weight: 1 / (days_since + 1)
        dt = commit_date(c)
        days = (now - dt).days
        stats["recency_score"] += 1.0 / (days + 1)

    # 4) Compute combined score and sort authors
    scored = [
        (login, stats["count"] + stats["recency_score"])
        for login, stats in author_stats.items()
    ]
    scored.sort(key=lambda x: x[1], reverse=True)

    # 5) Return top_n logins
    users = [login for login, _ in scored[:top_n]]
    return filter_human_users(users)
