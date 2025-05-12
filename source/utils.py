from urllib.parse import urlparse
import json
import re
from prettytable import PrettyTable
import textwrap


def parse_github_url(repo_url):
    parsed = urlparse(repo_url)
    parts = parsed.path.strip('/').split('/')
    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL format. Expected: https://github.com/owner/repo")
    return parts[0], parts[1]

def parse_full_repo_name(full_repo_name: str):

    FULL_REPO_NAME_PATTERN = re.compile(r'^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$')

    try:
        if not FULL_REPO_NAME_PATTERN.fullmatch(full_repo_name):
            raise ValueError(
                "Invalid format. Repo must match '<owner>/<repo>' "
                "using letters, numbers, '_', '-' or '.'."
            )
        owner, repo = full_repo_name.split('/', 1)
    except ValueError:
        raise ValueError("Input must be in the format 'owner/repo'")
    url = f"https://www.github.com/{owner}/{repo}"
    return url, owner, repo

def save_issues_to_file(issues, filename="issues.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(issues, f, indent=4)

def extract_keywords_from_json_string(text):
    pattern = r"```json\s*(\{.*?\})\s*```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        json_str = match.group(1)
        data = json.loads(json_str)
        return data["keywords"], data["summary"]
    return []


def get_bot_patterns():
    """
    Returns a list of regex patterns matching common non-human GitHub usernames.
    """
    return [
        r".*bot$",            # ends with “bot”
        r"^bot-.*",           # starts with “bot-”
        r".*bot-.*",          # contains “bot-”
        r".*\[bot\].*",          # contains “[bot]”
        r"dependabot.*",      # GitHub Dependabot
        r".*dependabot-.*",
        r".*[-_.]ci([-_.].*)?$",  # ci, .ci, -ci, _ci
        r".*actions?$",       # action or actions
        r"^web-flow$",        # GitHub’s web-flow alias
        r"^github-actions$",  # official GH Actions bot
        r".*automation.*",    # generic automation
        r"^pre-?commit$",     # pre-commit integrations
        r".*travis.*",        # Travis CI
        r".*circleci.*",      # CircleCI
        r".*mergify.*",       # Mergify
    ]

def is_bot_user(username, patterns=None):
    """
    Returns True if `username` matches any known bot/non-human pattern.
    """
    if patterns is None:
        patterns = get_bot_patterns()
    for pat in patterns:
        if re.match(pat, username, re.IGNORECASE):
            return True
    return False

def filter_human_users(user_list, patterns=None):
    """
    Filters out bot/non-human usernames from `user_list` using regex patterns.
    
    :param user_list:  List[str] of GitHub usernames
    :param patterns:   Optional override list of regex patterns
    :return:           List[str] containing only likely human usernames
    """
    return [u for u in user_list if not is_bot_user(u, patterns)]

def create_link_in_print(uri, label=None):
    if label is None:
        label = uri
    parameters = ''

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'

    return escape_mask.format(parameters, uri, label)

def print_issue_pretty(issue, wrap_width=60):
    """
    issue: dict with keys
      - issue_number (int)
      - title (str)
      - labels (list of str)
      - keywords (list of str)
      - summary (str)
    wrap_width: max characters per line in the Value column
    """
    # 1. Prepare the table
    table = PrettyTable()
    table.field_names = ["Field", "Value"]
    table.align["Field"] = "l"
    table.align["Value"] = "l"
    # Let PrettyTable wrap long text for us:
    table.max_width["Value"] = wrap_width
    table.header = False
    table.border = False

    # 2. Helper to wrap long strings
    def wrap(text):
        return "\n".join(textwrap.wrap(str(text), wrap_width))

    # 3. Add rows
    table.add_row(["Issue number", issue["issue_number"]])
    table.add_row(["", ""])
    table.add_row(["Title", wrap(issue["title"])])
    table.add_row(["", ""])
    table.add_row(["Labels", wrap(issue["labels"])])
    table.add_row(["", ""])
    table.add_row(["Keywords", wrap(issue["keywords"])])
    table.add_row(["", ""])
    table.add_row(["Summary", wrap(issue["summary"])])
    table.add_row(["", ""])

    # 4. Print
    print(table)