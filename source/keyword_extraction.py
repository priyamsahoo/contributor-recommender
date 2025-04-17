import json
import google.generativeai as genai
import os
from time import sleep
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)


def load_issues(file_path):
    """Load issues from JSON file"""
    with open(file_path, 'r') as f:
        return json.load(f)

def save_results(output_path, results):
    """Save extracted keywords to JSON file"""
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

def extract_keywords(issue, model="gemini-2.0-flash"):
    """Extract technical keywords using LLM"""
    prompt = f"""
    Role:
    You are an expert open-source project maintainer. Your job is to extract the most important technical keywords from GitHub issues.
    Focus on technical terms, filenames, modules, functions, error types, and important features.
    If the issue description is vague or unclear, make an intelligent guess based on common software engineering knowledge, but stay conservative.
    Input:
    You are given the title and description of a GitHub issue. The description may be detailed or vague.
    Steps:
    - Read the title and description carefully.
    - Focus on extracting technical keywords, such as:
        - Technical components (e.g., SSH, API, logging)
        - Programming languages or frameworks
        - Infrastructure components (e.g., cloud storage, servers)
        - Specific error types
        - Filenames, file paths, or modules if mentioned
        - Important features or version information
    - If the description is vague or missing technical terms, make an intelligent guess based on common software engineering knowledge, but stay conservative.
    - Only return keywords that are explicitly present or strongly implied.
    - Do not include random words, general English, or anything unrelated.

    Expectations:
    - Output only comma-separated keywords.
    - No extra explanation, sentences, or formatting.
    - If no technical keywords are found, return an empty string.

    Example:

    ---
    Example Input:

    Title:  "Reduce integration test dependencies on external resources"

    Body:"### Summary\n\nMany integration tests depend on external resources, aside from pip installed packages from PyPI and OS package installs. These dependencies should be replaced with local options where possible.\n\nExamples of dependencies to consider replacing:\n\n- File downloads, such as from the ci-files S3 bucket.\n\n- Use of external APIs, such as Galaxy.\n\n- Cloning of git repositories, usually from GitHub.\n\n- Installation of packages from alternative repositories.\n\nChanges should be backported through stable-2.14, when possible, particularly for tests run on RHEL..\n\n\n\n### Issue Type\n\nFeature Idea\n\n### Component Name\n\nintegration tests\n\n### Ansible Version\n\n```console\n$ ansible --version\n```\n\n### Configuration\n\n```console\n### OS / Environment\n\nlinux\n\n### Additional Information\n\n.\n\n### Code of Conduct\n\n- [x] I agree to follow the Ansible Code of Conduct"

    Expected Keywords/Output:
    integration tests, external dependencies, S3 bucket, ci-files, Galaxy API, Git repositories, package repositories, RHEL, backporting, Stable-2.14, dependency isolation, Feature idea, 

    ---
    Analyze this GitHub issue and extract relevant technical keywords:
    New Input:

    Title: {issue['title']}
    Description: {issue['body']}

    Extract and return only comma-separated technical keywords.
    """
    
    try:
        model = genai.GenerativeModel(model)
        response = model.generate_content(prompt)
        content = response.text.strip()
        # return response.choices[0].message['content'].strip().split(', ')
        keywords = [k.strip() for k in content.split(',')]
        return keywords, content

    except Exception as e:
        print(f"Error processing issue {issue['number']}: {str(e)}")
        return []

def process_single_issue(issues, issue_number, output_path):
    """Process a single issue selected by user input"""
    selected_issue = next((issue for issue in issues if issue['number'] == issue_number), None)
    
    if selected_issue is None:
        print(f"Issue #{issue_number} not found.")
        return

    print(f"Processing issue #{issue_number} - {selected_issue['title']}")

    keywords, _ = extract_keywords(selected_issue)

    result = {
        "issue_number": selected_issue["number"],
        "title": selected_issue["title"],
        "keywords": keywords,
        "labels": selected_issue.get("labels", [])
    }

    save_results(output_path, [result])
    print(f"Results saved to {output_path}")

# def process_issues(issues, output_path, delay=1):
#     results = []
    
#     for idx, issue in enumerate(issues):
#         print(f"Processing issue #{issue['number']} ({idx+1}/{len(issues)})")
        
#         keywords, _ = extract_keywords(issue)  # ignore raw_output now
#         results.append({
#             "issue_number": issue["number"],
#             "title": issue["title"],
#             "keywords": keywords,
#             "labels": issue.get("labels", [])
#         })
        
#         sleep(delay)
        
#     save_results(output_path, results)
#     return results

# if __name__ == "__main__":
#     issues = load_issues("issues.json")
#     process_issues(issues, "issues_with_keywords.json")
