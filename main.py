import os
import argparse
from dotenv import load_dotenv

from source.fuse_contributors import fuse_contributors
from source.get_contributor_from_file_changes import find_contributors_from_file_data
from source.github import list_github_issues
from source.get_contributors_BM25 import find_contributors
from source.utils import create_link_in_print, filter_human_users, parse_full_repo_name, parse_github_url, save_issues_to_file
from source.keyword_extraction import process_single_issue, load_issues
from source.print_colors import bcolors

def main():

    parser = argparse.ArgumentParser(
        prog="git-recommend",
        description="Fetch GitHub issues and recommend contributors that are most likely/capable to work on it"
    )

    parser.add_argument("full_repo_name", help="GitHub repository name with owner (e.g. owner/repo)")
    parser.add_argument("issue_number", type=int, help="Issue number to process")
    args = parser.parse_args()

    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    # repo_url = input("Enter GitHub repo URL to fetch issues from: ")

    full_repo_name = args.full_repo_name       # now comes from CLI
    issue_number = args.issue_number  # now comes from CLI

    try:
        # owner, repo = parse_github_url(repo_url)
        repo_url, owner, repo = parse_full_repo_name(full_repo_name)
        issues = list_github_issues(owner, repo, token=token)

        filename = f"{os.getcwd()}/outputs/{repo}_issues.json"
        save_issues_to_file(issues, filename)
        print(f"{bcolors.WARNING}Saved {len(issues)} issues to '{filename}'{bcolors.ENDC}\n")

        issues = load_issues(filename)
        output_filename = f"{os.getcwd()}/outputs/{repo}_issues_with_keywords.json"
        
        print(f"{bcolors.OKCYAN}Processing issue #{issue_number} from {owner}/{repo}...{bcolors.ENDC}\n")
        process_single_issue(issues, issue_number, output_filename)

        print(f"{bcolors.OKCYAN}Finding contributors...{bcolors.ENDC}\n")

        # find contributors based on PR
        user_list_1 = find_contributors(
            owner,
            repo,
            token,
            keywords_file=output_filename,
            pr_count=500,
            top_n=5
        )
        top_users_based_on_prs = filter_human_users(user_list_1)

        print(f"{bcolors.OKBLUE}Top contributors based on who raised related PRs:{bcolors.ENDC}")
        for i, user in enumerate(top_users_based_on_prs, start=1):
            print(f"{i}. {user}")

        print()

        # find contributors from related file changes
        user_list_2 = find_contributors_from_file_data(
            token,
            output_filename,
            owner,
            repo)
        top_users_based_on_files_changed = filter_human_users(user_list_2)

        print(f"{bcolors.OKBLUE}Top contributors based on who worked on related code:{bcolors.ENDC}")
        for i, user in enumerate(top_users_based_on_files_changed, start=1):
            print(f"{i}. {user}")

        print()

        # rank contributors from both lists (via Reciprocal Rank Fusion)
        top_contributors = fuse_contributors(top_users_based_on_prs, top_users_based_on_files_changed)
        print(f"{bcolors.OKGREEN}{bcolors.BOLD}Most likely users to contribute to this issue are:{bcolors.ENDC}")
        for i, user in enumerate(top_contributors, start=1):
            # create a hyperlink to the users profile as well
            print(f"{bcolors.OKGREEN}{i}. {create_link_in_print(f'https://www.github.com/{user}', user)}")


        # else:
        #     print("Keyword extraction skipped.")
    except Exception as e:
        print(f"{bcolors.FAIL}Error: {e}{bcolors.ENDC}")

if __name__ == "__main__":
    main()
