import os
from dotenv import load_dotenv
from github import list_github_issues
from utils import parse_github_url, save_issues_to_file

def main():
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    repo_url = input("Enter GitHub repo URL to fetch issues from: ")

    try:
        owner, repo = parse_github_url(repo_url)
        issues = list_github_issues(owner, repo, token=token)
        filename = f"../Outputs/{repo}_issues.json"
        save_issues_to_file(issues, filename)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
