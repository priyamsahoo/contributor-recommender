# contributor-recommender: An LLM-Assisted Open-Source Issue Summarizer and Contributor Finder
A tool that analyzes open-source issues, summarizes them and finds relevant contributors to solve the issues

## Introduction  
The project is a command-line utility `command: git-recommend` that automates issue triage by generating concise summaries and extracting key technical terms from GitHub issues, then analyzes repository history to recommend the most relevant contributors. It combines LLM-driven keyword extraction and summarization with both pull-request and file-blame ranking strategies, merging them via Reciprocal Rank Fusion (RRF) to produce a ranked list of handles and relevance scores—all within your terminal.

## How to Use

1. **Token creation**  
   1. **GitHub API token**: follow GitHub’s guide to create a Personal Access Token with at least `repo` and `read:org` scopes:  
      [GitHub API](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
   2. **Google AI Studio key**: sign in to Google AI Studio and generate an API key:  
      [Google AI Studio API Key](https://aistudio.google.com/app/apikey)

3. **Clone the repository**

   ```bash
   git clone https://github.com/priyamsahoo/contributor-recommender.git
   ```

4. **Change into the project directory**

   ```bash
   cd contributor-recommender
   ```

5. **[Optional] Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

6. **Install in “editable” mode**

   ```bash
   pip install -e .
   ```

7. **Verify the installation**

   ```bash
   git-recommend --help
   ```

   You should see output similar to:

   ```
    usage: git-recommend [-h] full_repo_name issue_number

    Fetch GitHub issues and recommend contributors that are most likely/capable to work on it

    positional arguments:
    full_repo_name  GitHub repository name with owner (e.g. owner/repo)
    issue_number    Issue number to process

    options:
    -h, --help      show this help message and exit
   ```

8. **Run the tool**

   ```bash
   git-recommend <owner>/<repo> <issue_number>
   ```

   Example:

   ```bash
   git-recommend ansible/vscode-ansible 1988
   ```

9. **View generated artifacts**
   All intermediate files (summaries, keyword lists, ranking data) are saved under the `outputs/` directory for your inspection.

## Issues and Contributions

### Reporting an Issue

* Navigate to this repository’s **Issues** tab.
* Click **New issue**.
* Select the appropriate template (bug report, feature request, etc.).
* Provide a clear title and detailed description of the problem or request.
* Submit the issue.

### Contributing

* **Fork** the repository to your own GitHub account.
* **Clone** your fork locally:

  ```bash
  git clone https://github.com/<your-username>/contributor-recommender.git
  ```
* **Create** a new branch for your changes:

  ```bash
  git checkout -b feature/your-feature-name
  ```
* **Implement** your changes, add tests if applicable, and update documentation.
* **Commit** your work with a descriptive message:

  ```bash
  git commit -m "Add feature X: description"
  ```
* **Push** your branch to your fork:

  ```bash
  git push origin feature/your-feature-name
  ```
* **Open** a Pull Request against the upstream `main` branch.
* Ensure your PR includes

  * A clear description of what you changed and why
  * Reference to any related issue(s)
  * Passing CI checks and adherence to coding standards

Thank you for helping improve this tool!

