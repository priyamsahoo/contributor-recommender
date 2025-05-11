def fuse_contributors(prs_ranked, files_ranked, k=60, top_n=3):
    """
    Combine two ranked lists of GitHub users (from PR history and file-change history)
    via Reciprocal Rank Fusion, and return the top_n contributors.

    :param prs_ranked:   List[str] – users ranked by related-PRs relevance
    :param files_ranked: List[str] – users ranked by file-change relevance
    :param k:            float    – RRF damping constant (default: 60)
    :param top_n:        int      – how many top contributors to return
    :return:             List[str] – fused top_n users
    """
    scores = {}

    # helper to add RRF scores from one list
    def add_scores(ranked_list):
        for idx, user in enumerate(ranked_list, start=1):
            scores[user] = scores.get(user, 0.0) + 1.0 / (k + idx)

    # fuse both rankings
    add_scores(prs_ranked)
    add_scores(files_ranked)

    # sort by descending score
    fused = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)

    # extract just the usernames
    return [user for user, _ in fused[:top_n]]


'''
How it works:

1. Rank→Score conversion
   Each user’s position r in a list contributes 1/(k+r).

2. Aggregation
   We sum those contributions across both lists.

3. Final ranking
   Sorting by this fused score brings forward users who appear highly in either list, with
   a bias toward those ranked near the top in both.

Adjust k to control how sharply you favor top positions (smaller k → steeper drop-off).
'''