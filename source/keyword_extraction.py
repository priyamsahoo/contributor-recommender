import json
import google.generativeai as genai
import os
from time import sleep
from dotenv import load_dotenv
from source.keyword_extraction_prompt import contruct_prompt
from source.print_colors import bcolors
from source.utils import extract_keywords_from_json_string

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
   
    prompt = contruct_prompt(issue)
    
    try:
        model = genai.GenerativeModel(model)
        response = model.generate_content(prompt)
        content = response.text.strip()
        # return response.choices[0].message['content'].strip().split(', ')
        if(content.startswith("```json")):
            keywords = keywords = extract_keywords_from_json_string(content)
        else:
            keywords = [k.strip() for k in content.split(',')]
        return keywords, content

    except Exception as e:
        print(f"Error processing issue {issue['number']}: {str(e)}")
        return []

def process_single_issue(issues, issue_number, output_path):
    """Process a single issue selected by user input"""
    selected_issue = next((issue for issue in issues if issue['number'] == issue_number), None)
    
    if selected_issue is None or selected_issue["state"] == "closed":
        raise Exception(f"Issue #{issue_number} is either closed or does not exist.")
    
    keywords, _ = extract_keywords(selected_issue)

    result = {
        "issue_number": selected_issue["number"],
        "title": selected_issue["title"],
        "keywords": keywords,
        "labels": selected_issue.get("labels", [])
    }

    save_results(output_path, [result])

    print("Issue Number:", result["issue_number"])
    print("Title:", result["title"])
    print("Keywords:", result["keywords"])
    print("Labels:", result["labels"])

    print(f"{bcolors.WARNING}Results saved to {output_path}{bcolors.ENDC}\n")

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
