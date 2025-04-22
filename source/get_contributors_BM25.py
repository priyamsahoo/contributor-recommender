# get_contributors.py

# Requires: pip install rank-bm25
from rank_bm25 import BM25Okapi
import json
import requests

def find_contributors(owner, repo, token, keywords_file, pr_count=500, top_n=5):
    """
    Fetches the latest `pr_count` closed PRs from the given GitHub repo,
    scores them against the keywords in `keywords_file` using BM25,
    and returns the top_n contributor usernames.
    """

    with open(keywords_file, 'r', encoding='utf-8') as f:
        entries = json.load(f)
    kws = set()
    for e in entries:
        kws.update(e.get("keywords", []))
    keyword_doc = " ".join(kws).lower().split()


    headers = {"Authorization": f"token {token}"}
    prs = []
    per_page = 100
    page = 1
    while len(prs) < pr_count:
        params = {
            "state":      "closed",
            "per_page":   per_page,
            "page":       page,
            "sort":       "updated",
            "direction":  "desc"
        }
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
        r = requests.get(url, headers=headers, params=params)
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        prs.extend(batch)
        page += 1
    prs = prs[:pr_count]


    docs_tokens = []
    authors = []
    for pr in prs:
        text = pr.get("title", "")
        if pr.get("body"):
            text += " " + pr["body"]
        tokens = text.lower().split()
        docs_tokens.append(tokens)
        authors.append(pr["user"]["login"])


    bm25 = BM25Okapi(docs_tokens)
    scores = bm25.get_scores(keyword_doc)


    author_scores = {}
    for author, score in zip(authors, scores):
        author_scores[author] = author_scores.get(author, 0.0) + score


    top = sorted(author_scores.items(), key=lambda kv: kv[1], reverse=True)[:top_n]
    return [author for author, _ in top]
