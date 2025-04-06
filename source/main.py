import os
from dotenv import load_dotenv
from github import list_github_issues
from utils import parse_github_url, save_issues_to_file
from keyword_extraction import process_single_issue, load_issues

def main():
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    repo_url = input("Enter GitHub repo URL to fetch issues from: ")

    try:
        owner, repo = parse_github_url(repo_url)
        issues = list_github_issues(owner, repo, token=token)
        filename = f"../outputs/{repo}_issues.json"
        save_issues_to_file(issues, filename)
        #keywords extraction
        choice = input("Do you want to extract keywords from a specific issue now? (y/n): ").strip().lower()
        
        if choice == "y":
            issues = load_issues(filename)
            issue_number = int(input("Enter the issue number you want to process: "))
            output_filename = f"../outputs/{repo}_issues_with_keywords.json"
            process_single_issue(issues, issue_number, output_filename)
        else:
            print("Keyword extraction skipped.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
